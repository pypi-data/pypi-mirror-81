# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
CLI to select various configuration options

Currently just profiles
"""

import argparse
import os
import sys
import traceback
from logging import error
from .log import init_logger, add_logging_arguments
from .repo.metadata import get_profiles
from .colour import lblue, bright, green
from .globals import env
from .news import add_news_parsers
from .modules import add_parsers, handle_cfg_protect
from .l10n import l10n


def add_profile_parsers(subparsers):
    profile = subparsers.add_parser("profile", help=l10n("profile-help"))
    profile_subparsers = profile.add_subparsers()
    profile_list = profile_subparsers.add_parser("list", help=l10n("profile-list-help"))
    profile_set = profile_subparsers.add_parser("set", help=l10n("profile-set-help"))
    profile_set.add_argument("NUM", help=l10n("profile-number-help"))
    profile_show = profile_subparsers.add_parser("show", help=l10n("profile-show-help"))

    def get_profile():
        linkpath = os.path.join(env.PORTMOD_CONFIG_DIR, "profile")
        if os.path.exists(linkpath) and os.path.islink(linkpath):
            return os.readlink(linkpath).split("profiles")[-1].lstrip(os.path.sep)
        return None

    def list_func(args):
        profiles = get_profiles()
        padding = len(str(len(profiles)))
        print(bright(green(l10n("profile-available"))))
        for index, (_, profile, stability) in enumerate(profiles):
            selected = ""
            if get_profile() == profile:
                selected = lblue("*")
            print(
                "  {} {} ({})".format(
                    bright("[" + str(index) + "]"),
                    " " * (padding - len(str(index))) + profile,
                    stability,
                ),
                selected,
            )

    def set_func(args):
        os.makedirs(env.PORTMOD_CONFIG_DIR, exist_ok=True)
        linkpath = os.path.join(env.PORTMOD_CONFIG_DIR, "profile")
        if os.path.exists(linkpath):
            os.unlink(linkpath)
        (path, _, _) = get_profiles()[int(args.NUM)]
        os.symlink(path, linkpath)

    def show_func(args):
        linkpath = os.path.join(env.PORTMOD_CONFIG_DIR, "profile")
        print(bright(green(l10n("profile-current-symlink", path=linkpath))))
        print(
            "  "
            + bright(os.readlink(linkpath).split("profiles")[-1].lstrip(os.path.sep))
        )

    def profile_help(args):
        profile.print_help()

    profile.set_defaults(func=profile_help)
    profile_list.set_defaults(func=list_func)
    profile_set.set_defaults(func=set_func)
    profile_show.set_defaults(func=show_func)


def main():
    """
    Main function for the omwselect executable
    """
    parser = argparse.ArgumentParser(description=l10n("select-help"))
    parser.add_argument("--debug", help=l10n("debug-help"), action="store_true")
    subparsers = parser.add_subparsers()
    add_profile_parsers(subparsers)
    add_news_parsers(subparsers)
    add_logging_arguments(parser)
    add_parsers(subparsers)

    args = parser.parse_args()
    init_logger(args)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    if args.debug:
        env.DEBUG = True
    try:
        args.func(args)
        handle_cfg_protect()
    except Exception as e:
        traceback.print_exc()
        error("{}".format(e))
        sys.exit(1)
