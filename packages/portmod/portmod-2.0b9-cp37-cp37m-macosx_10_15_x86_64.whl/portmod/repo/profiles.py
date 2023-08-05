# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from typing import List, Set
from pathlib import Path
from ..globals import env
from .atom import Atom
from .list import read_list


def profile_exists() -> bool:
    return os.path.exists(os.path.join(env.PORTMOD_CONFIG_DIR, "profile"))


def get_profile_path() -> str:
    """Returns the path to the profile directory"""
    profilepath = os.path.join(env.PORTMOD_CONFIG_DIR, "profile")
    if not os.path.exists(profilepath) or not os.path.islink(profilepath):
        raise Exception(
            f"{profilepath} does not exist.\n"
            "Please choose a profile before attempting to install mods"
        )
    # Note: Path must be resolved with pathlib to ensure that
    # the path doesn't include \\?\ on Windows
    return str(Path(os.readlink(profilepath)).resolve())


def profile_parents() -> List[str]:
    """
    Produces the paths of all the parent directories for the selected profile, in order
    """
    first = get_profile_path()

    def get_parents(directory: str) -> List[str]:
        parentfile = os.path.join(directory, "parent")
        parents = []
        if os.path.exists(parentfile):
            for parent in read_list(parentfile):
                parentpath = os.path.normpath(os.path.join(directory, parent))
                parents.extend(get_parents(parentpath))
                parents.append(parentpath)

        return parents

    parents = [first]
    parents.extend(get_parents(first))

    userpath = os.path.join(env.PORTMOD_CONFIG_DIR, "profile.user")
    if os.path.exists(userpath):
        parents.append(userpath)
        parents.extend(get_parents(userpath))

    return parents


def get_system() -> Set[Atom]:
    """Calculates the system set using the user's currently selected profile"""
    system: Set[Atom] = set()
    for parent in profile_parents():
        mods = os.path.join(parent, "mods")
        if os.path.exists(mods):
            system |= {
                Atom(mod.lstrip("*")) for mod in read_list(mods) if mod.startswith("*")
            }

    return system
