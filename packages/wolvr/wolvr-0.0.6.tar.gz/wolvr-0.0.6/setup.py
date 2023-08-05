# -*- coding: utf-8 -*-

# Author: Tom Bresee <tbresee@umich.edu>
#
# License: BSD 3 clause


import setuptools

import wolvr

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    required = fh.read().splitlines()


setuptools.setup(
    name="wolvr",
    version="0.0.6",
    author="Tom Bresee",
    author_email="tbresee@umich.edu",
    description="Utility Belt for Machine Learning",
    license="BSD 3-Clause",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/tombresee/wolvr",
    packages=setuptools.find_packages(),
    classifiers=[  # https://pypi.org/classifiers/
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
    include_package_data=True,
)
