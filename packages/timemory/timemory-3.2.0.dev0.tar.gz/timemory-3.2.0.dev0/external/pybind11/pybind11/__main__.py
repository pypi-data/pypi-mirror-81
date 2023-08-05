# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import sys
import sysconfig

from .commands import get_include, get_cmake_dir


def print_includes():
    dirs = [
        sysconfig.get_path("include"),
        sysconfig.get_path("platinclude"),
        get_include(),
    ]

    # Make unique but preserve order
    unique_dirs = []
    for d in dirs:
        if d not in unique_dirs:
            unique_dirs.append(d)

    print(" ".join("-I" + d for d in unique_dirs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--includes",
        action="store_true",
        help="Include flags for both pybind11 and Python headers.",
    )
    parser.add_argument(
        "--cmakedir",
        action="store_true",
        help="Print the CMake module directory, ideal for setting -Dpybind11_ROOT in CMake.",
    )
    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
    if args.includes:
        print_includes()
    if args.cmakedir:
        print(get_cmake_dir())


if __name__ == "__main__":
    main()
