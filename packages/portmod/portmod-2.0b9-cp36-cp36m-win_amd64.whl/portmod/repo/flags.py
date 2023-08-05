# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Iterable, Optional, Set
import os
import re
from logging import info
from portmod.repo.atom import Atom, atom_sat
from .list import read_list
from ..l10n import l10n


def get_flags(file: str, atom: Optional[Atom] = None) -> Set[str]:
    """
    Reads flags from a given file.
    If the atom argument is passed, file is assumed to be newline delimited
    with an atom followed by a list of flags on each line.
    If atom is None, file is assumed to be a newline delimited list of flags
    """
    flags = []
    if os.path.exists(file):
        for line in read_list(file):
            # Remove comments
            line = re.sub("#.*", "", line)
            if not line:
                continue

            if atom:
                elem = line.split()
                flags.append((Atom(elem[0]), elem[1:]))
            else:
                flags.append(line)
    else:
        return set()

    if atom:
        atom_flags: Set[str] = set()
        for (a, flaglist) in flags:
            if atom_sat(atom, a):
                atom_flags = collapse_flags(atom_flags, flaglist)
        return atom_flags

    return collapse_flags(set(), flags)


def collapse_flags(old: Iterable[str], new: Iterable[str]) -> Set[str]:
    """
    Collases an ordered list of flags into an unordered set of flags
    """
    newset = set(old)
    for flag in new:
        if not flag.startswith("-"):
            newset.discard(f"-{flag}")
        elif flag.startswith("-"):
            newset.discard(flag.lstrip("-"))
        newset.add(flag)
    return newset


def add_flag(file, atom, flag):
    if os.path.exists(file):
        flagfile = __read_flags(file)
    else:
        flagfile = []

    found = False
    for (index, line) in enumerate(flagfile):
        tokens = line.split()
        if tokens[0] == atom:
            if flag not in tokens:
                info(l10n("flag-add", flag=flag, atom=atom, file=file))
                flagfile[index] = "{} {}".format(line, flag)
            found = True
    if not found:
        info(l10n("flag-add", flag=flag, atom=atom, file=file))
        flagfile.append("{} {}".format(atom, flag))

    __write_flags(file, flagfile)


def remove_flag(file, atom, flag):
    flagfile = __read_flags(file)

    for (index, line) in enumerate(flagfile):
        tokens = line.split()
        if atom_sat(Atom(tokens[0]), atom) and flag in tokens:
            info(l10n("flag-remove", flag=flag, atom=atom, file=file))
            tokens = list(filter(lambda a: a != flag, tokens))

            if len(tokens) > 1:
                flagfile[index] = " ".join(tokens)
            else:
                del flagfile[index]

    __write_flags(file, flagfile)


def __read_flags(file):
    if os.path.exists(file):
        with open(file, mode="r") as flagfile:
            return flagfile.read().splitlines()
    return []


def __write_flags(file, new_flagfile):
    with open(file, mode="w") as flagfile:
        for line in new_flagfile:
            print(line, file=flagfile)
