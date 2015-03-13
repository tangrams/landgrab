# -*- coding: utf-8 -*-


# import everything from cPolygon
from cPolygon import *

# keep namespace clean
__version__ = version
__author__  = author
__license__ = license
del version, author, license


# support functions for pickling and unpickling
def __createPolygon(contour, hole):
    """rebuild Polygon from pickled data"""
    p = Polygon()
    map(p.addContour, contour, hole)
    return p


def __tuples(a):
    """map an array or list of lists to a tuple of tuples"""
    return tuple(map(tuple, a))


def __reducePolygon(p):
    """return pickle data for Polygon """
    return (__createPolygon, (tuple([__tuples(x) for x in p]), p.isHole()))


import copy_reg
copy_reg.constructor(__createPolygon)
copy_reg.pickle(Polygon, __reducePolygon)
del copy_reg

