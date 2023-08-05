# -*- coding: utf-8 -*-

# Author: Tom Bresee <tbresee@umich.edu>
#
# License: BSD 3 clause

from ._naive_bayes import naive_bayes_Bernoulli, naive_bayes_multinomial, naive_bayes_Gaussian, demo

# this is for "from <package_name>.naive_bayes import *"
__all__ = ["naive_bayes_Bernoulli",
           "naive_bayes_multinomial",
           "naive_bayes_Gaussian",
           "demo"]
