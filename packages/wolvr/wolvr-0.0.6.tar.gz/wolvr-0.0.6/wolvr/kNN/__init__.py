# -*- coding: utf-8 -*-

# Author: Tom Bresee <tbresee@umich.edu>
#
# License: BSD 3 clause

from ._kNN import kNN_classifier, demo

# this is for "from <package_name>.kNN import *"
__all__ = ["kNN_classifier", "demo"]
