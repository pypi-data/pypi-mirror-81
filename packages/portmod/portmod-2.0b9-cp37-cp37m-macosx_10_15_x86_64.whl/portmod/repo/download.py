# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import AbstractSet, Dict, Iterable, List, Optional

import os
import urllib
import urllib.parse
import logging
from logging import info
from base64 import b64decode, b16encode

from portmod.repo.util import get_hash
from portmod.globals import env
from ..config import get_config
from ..pybuild import FullPybuild, Pybuild, Source, HashAlg, MD5
from ..repos import get_repo
from .metadata import get_license_groups, get_repo_root
from .usestr import use_reduce
from .use import get_use
from ..l10n import l10n


class RemoteHashError(Exception):
    """Exception indicating an unexpected download file"""


class LocalHashError(Exception):
    """Exception indicating an unexpected download file"""


def parse_arrow(sourcelist: Iterable[str]) -> List[Source]:
    """
    Turns a list of urls using arrow notation into a list of
    Source objects
    """
    result: List[Source] = []
    arrow = False
    for value in sourcelist:
        if arrow:
            result[-1] = Source(result[-1].url, value)
            arrow = False
        elif value == "->":
            arrow = True
        else:
            url = urllib.parse.urlparse(value)
            result.append(Source(value, os.path.basename(url.path)))
    return result


def get_filename(basename: str, path: Optional[str] = None) -> str:
    """
    By default returns the location of the local cached version of the source
    file corresponding to the given name. The file may or may not exist.
    @return full path of file combined from path and basename
    """
    if not path:
        path = env.DOWNLOAD_DIR
    return os.path.join(path, basename)


def mirrorable(mod: Pybuild, enabled_use: Optional[AbstractSet[str]] = None) -> bool:
    """
    Returns whether or not a mod can be mirrored
    """
    # FIXME: Determine which sources have use requirements
    # that don't enable mirror or fetch
    if "mirror" not in mod.RESTRICT and "fetch" not in mod.RESTRICT:
        redis: Iterable[str]
        if mod.INSTALLED:
            redis = get_license_groups(get_repo(mod.REPO).location).get(
                "REDISTRIBUTABLE", []
            )
        else:
            redis = get_license_groups(get_repo_root(mod.FILE)).get(
                "REDISTRIBUTABLE", []
            )

        def is_license_redis(group):
            if not group:
                # No license is considered equivalent to all-rights-reserved
                return False
            if isinstance(group, str):
                return group in redis
            if group[0] == "||":
                return any(is_license_redis(li) for li in group)

            return all(is_license_redis(li) for li in group)

        if enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, enabled_use, opconvert=True)
        ):
            return True
        if not enabled_use and is_license_redis(
            use_reduce(mod.LICENSE, opconvert=True, matchall=True)
        ):
            return True

    return False


def fetchable(mod: FullPybuild) -> List[Source]:
    """
    Returns the list of fetchable sources associated with a mod
    A source can be fetched if it is mirrorable,
    or if it has a URI
    """
    if "fetch" in mod.RESTRICT:
        return []

    use, _ = get_use(mod)
    if "mirror" not in mod.RESTRICT and mirrorable(mod, use):
        return mod.get_default_sources()

    can_fetch = []
    for source in mod.get_default_sources():
        parsedurl = urllib.parse.urlparse(source.url)
        if parsedurl.scheme:
            can_fetch.append(source)

    return can_fetch


def progress_write(request, filepath, start=0, mode="wb", size: Optional[int] = None):
    from progressbar import Bar, ETA, FileTransferSpeed, Percentage, ProgressBar

    bytes = start
    bar = ProgressBar(
        widgets=[Percentage(), " ", Bar(), " ", ETA(), " ", FileTransferSpeed()],
        redirect_srdout=True,
        max_value=size,
    )

    bar.start()
    with open(filepath, mode=mode) as file:
        for buf in request.iter_content(1024):
            if buf:
                file.write(buf)
                bytes += len(buf)
                bar.update(bytes)
    bar.finish()


def get_remote_size(request):
    if "Content-Length" in request.headers:
        return int(request.headers["Content-Length"].strip())
    else:
        return None


def get_remote_hashes(request):
    header = "X-Goog-Hash"
    remote_hashes = {}

    if header in request.headers:
        for remote_hash in request.headers[header].split(", "):
            hash = remote_hash.split("=", maxsplit=1)
            remote_hashes[hash[0]] = hash[1]
        if "md5" in remote_hashes:
            remote_hashes["md5"] = (
                b16encode(b64decode(remote_hashes["md5"])).decode("utf-8").lower()
            )

    return remote_hashes


def download(
    url: str,
    dest_name: str,
    *,
    size: Optional[int] = None,
    hashes: Dict[HashAlg, str] = {},
    dest_path: Optional[str] = None,
):
    """
    Downloads the given url to the dest_path
    """
    # Slow imports
    import requests

    print(l10n("fetching", url=url))

    if not dest_path:
        dest_path = env.DOWNLOAD_DIR

    os.makedirs(dest_path, exist_ok=True)

    req = requests.get(url, stream=True)
    req.raise_for_status()

    precheck = False
    remote_size = get_remote_size(req)
    remote_hashes = get_remote_hashes(req)

    if "md5" in remote_hashes and MD5 in hashes:
        precheck = True
        remote_hash = remote_hashes["md5"]
        if hashes[MD5] != remote_hash:
            raise RemoteHashError(
                l10n("remote-hash-mismatch", hash1=hashes[MD5], hash2=remote_hash)
            )

    file = get_filename(dest_name, dest_path)
    progress_write(req, file, size=remote_size or size)

    if remote_size:
        filesize = os.path.getsize(file)
        while filesize < remote_size:
            req = requests.get(
                url, stream=True, headers={"Range": "bytes=%d-" % filesize}
            )
            progress_write(req, file, start=filesize, mode="ab", size=remote_size)
            filesize = os.path.getsize(file)

    # Skip post check if we did a pre-check using a local hash
    if not precheck and "md5" in remote_hashes:
        localhash = get_hash(get_filename(dest_name), (MD5.func,))[0]
        if localhash != remote_hashes["md5"]:
            # Try again
            download(url, dest_name, size=size, hashes=hashes, dest_path=dest_path)


def check_hash(filename: str, hashes: Dict[HashAlg, str], raise_ex=False) -> bool:
    """
    Returns true if and only if the sha512sum of the given file
    matches the given checksum
    """
    results = get_hash(filename, tuple([h.func for h in sorted(hashes)]))
    for halg, result in zip(sorted(hashes), results):
        if hashes[halg] != result:
            if raise_ex:
                raise LocalHashError(
                    l10n(
                        "local-hash-mismatch",
                        filename=filename,
                        hash=halg.name,
                        hash1=hashes[halg],
                        hash2=result,
                    )
                )
            return False
    return True


def get_download(name: str, hashes: Optional[Dict[HashAlg, str]]) -> Optional[str]:
    src = find_download(name, hashes)
    if src:
        dest = get_filename(name)
        if src == dest:
            return dest

        info(l10n("file-moving", src=src, dest=dest))
        os.rename(src, dest)
        return dest


def find_download(name: str, hashes: Optional[Dict[HashAlg, str]]) -> Optional[str]:
    """
    Determines if the given file is in the cache.
    The file must match both name and checksum
    @return path to donloaded file
    """

    def find_by_name(directory: str):
        if os.path.exists(directory):
            src = os.path.join(directory, name)
            if os.path.exists(src) and (hashes is None or check_hash(src, hashes)):
                return src

            # If a file with spaces otherwise matches use it
            for file in os.listdir(directory):
                src = os.path.join(directory, file)
                if file.replace(" ", "_") == name:
                    try:
                        if hashes is None or check_hash(src, hashes, raise_ex=True):
                            return src
                    except LocalHashError as e:
                        logging.warning(
                            l10n(
                                "possible-local-hash-mismatch", filename=file, name=name
                            )
                            + f": {e}"
                        )

    return (
        find_by_name(env.DOWNLOAD_DIR)
        or find_by_name(os.path.expanduser(os.path.join("~", "Downloads")))
        or find_by_name(os.environ.get("DOWNLOADS", ""))
    )


def is_downloaded(mod: FullPybuild) -> bool:
    """
    Returns true if all the mod's sources can be found
    """
    for source in mod.get_default_sources():
        cached = find_download(source.name, source.hashes)
        if cached is None:
            return False
    return True


def download_and_check(url: str, source: Source, *, try_again: bool = True) -> str:
    download(url, source.name, size=source.size, hashes=source.hashes)
    filename = get_filename(source.name)

    try:
        check_hash(filename, source.hashes, raise_ex=True)
    except LocalHashError as e:
        if try_again:  # Try again once if download fails
            logging.error(e)
            print(l10n("retrying-download", url=url))
            download_and_check(url, source, try_again=False)
        else:
            raise


def download_source(mod, source: Source, check: bool = True) -> str:
    """
    Downloads the given source file.
    @return the path to the downloaded source file
    """
    # Slow import
    import requests

    if check:
        cached = get_download(source.name, source.hashes)
    else:
        cached = get_download(source.name, None)
    fetch = "fetch" not in mod.get_restrict()
    mirror = (
        "mirror" not in mod.get_restrict()
        and "fetch" not in mod.get_restrict()
        and mirrorable(mod)
    )

    if cached:
        # Download is in cache. Nothing to do.
        return cached
    elif not fetch:
        # Mod cannot be fetched and is not already in cache. abort.
        raise Exception(l10n("source-unfetchable", source=source))
    else:
        parsedurl = urllib.parse.urlparse(source.url)

        # Download archive
        filename = get_filename(source.name)

        if mirror:
            PORTMOD_MIRRORS = get_config()["PORTMOD_MIRRORS"].split()
            for mirror_url in PORTMOD_MIRRORS:
                try:
                    url = urllib.parse.urljoin(mirror_url, source.name)

                    if check:
                        download_and_check(url, source)
                    else:
                        download(
                            url, source.name, size=source.size, hashes=source.hashes
                        )

                    return filename
                except requests.exceptions.HTTPError as err:
                    if parsedurl.scheme:
                        logging.info(f"{err}")
                    else:  # If there is no original source, warn instead of info
                        logging.warning(f"{err}")

        if parsedurl.scheme != "":
            if check:
                download_and_check(source.url, source)
            else:
                download(
                    source.url, source.name, size=source.size, hashes=source.hashes
                )

            return filename

        raise Exception(l10n("source-unfetchable", source=source))


def download_mod(mod: FullPybuild, matchall=False) -> List[Source]:
    """
    Downloads missing sources for the given mod in its current USE configuration
    @return A list of paths of the sources for the mod
    """
    download_list = []
    if matchall:
        sources = mod.get_sources(matchall=True)
    else:
        sources = mod.get_default_sources()

    for source in sources:
        download_source(mod, source)

        download_list.append(source)

    return download_list
