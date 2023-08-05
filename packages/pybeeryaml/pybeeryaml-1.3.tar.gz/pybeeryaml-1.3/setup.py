#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""PyBeerYAML A YAML format parser for beer storage"""

# Pybeeryaml
# Copyright (C) 2018  TROUVERIE Joachim <joachim.trouverie@linoame.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

__version__ = "1.3"
__author__ = "TROUVERIE Joachim"
__email__ = "jtrouverie@joakode.fr"
__url__ = "https://github.com/j0ack/pybeeryaml"

requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

with open('README.rst', 'r') as fi:
    long_description = fi.read()

setup(
    name="pybeeryaml",
    packages=find_packages(),
    version=__version__,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=__author__,
    author_email=__email__,
    url="https://pythonhosted.org/pybeeryaml/",
    download_url=__url__,
    install_requires=requirements,
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
