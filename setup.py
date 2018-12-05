#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():
    setuptools.setup(
        name             = "tumblr_dl",
        version          = "2018.12.05.1548",
        description      = "download media of Tumblr subdomains",
        long_description = long_description(),
        url              = "https://github.com/wdbm/tumblr_dl",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        packages         = setuptools.find_packages(),
        install_requires = [
                           "docopt"
                           ],
        entry_points     = {
                           "console_scripts": ("tumblr_dl = tumblr_dl.__init__:main")
                           },
        zip_safe         = False
    )

def long_description(
    filename = "README.md"
    ):
    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
