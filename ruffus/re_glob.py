"""Filename globbing utility."""

import sys
import os
import re

__all__ = ["re_glob", "ire_glob"]

def re_glob(pathname):
    """Return a list of paths matching a pathname pattern using regular expresions

    """
    return list(ire_glob(pathname))

def ire_glob(pathname):
    """Return an iterator which yields the paths matching a pathname pattern using regular expresions
    """
    if not has_magic(pathname):
        if os.path.lexists(pathname):
            yield pathname
        return
    dirname, basename = os.path.split(pathname)
    if not dirname:
        for name in re_glob1(os.curdir, basename):
            yield name
        return
    if has_magic(dirname):
        dirs = ire_glob(dirname)
    else:
        dirs = [dirname]
    if has_magic(basename):
        re_glob_in_dir = re_glob1
    else:
        re_glob_in_dir = re_glob0
    for dirname in dirs:
        for name in re_glob_in_dir(dirname, basename):
            yield os.path.join(dirname, name)

# These 2 helper functions non-recursively re_glob inside a literal directory.
# They return a list of basenames. `re_glob1` accepts a pattern while `re_glob0`
# takes a literal basename (so it only has to check for its existence).

def re_glob1(dirname, pattern):
    if not dirname:
        dirname = os.curdir
    if isinstance(pattern, unicode) and not isinstance(dirname, unicode):
        dirname = unicode(dirname, sys.getfilesystemencoding() or
                                   sys.getdefaultencoding())
    try:
        names = os.listdir(dirname)
    except os.error:
        return []
    if pattern[0] != '.':
        names = filter(lambda x: x[0] != '.', names)
    
    # only where entire name is specified by regular expression    
    matching = []
    for n in names:
        m = re.match(pattern, n)
        if m and m.end() == len(n):
            matching.append(n)
    return matching

def re_glob0(dirname, basename):
    if basename == '':
        # `os.path.split()` returns an empty basename for paths ending with a
        # directory separator.  'q*x/' should match only directories.
        if os.path.isdir(dirname):
            return [basename]
    else:
        if os.path.lexists(os.path.join(dirname, basename)):
            return [basename]
    return []


magic_check = re.compile('[.*\\\^$?(){}[\]]')

def has_magic(s):
    return magic_check.search(s) is not None
