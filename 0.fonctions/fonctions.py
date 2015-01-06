# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:22:38 2015

@author: roms
"""

import math

def toXY(longitude, latitude):
    x = longitude * 1000
    y = latitude * 1000
    return x, y

def toLongLat(x, y):
    longitude = x / 1000
    latitude = y / 1000
    return longitude, latitude

def distance(a1, b1, a2, b2, type_):
    if(type_ == 0):
        longitude1 = a1
        latitude1 = b1
        longitude2 = a2
        latitude2 = b2
        return math.sqrt((longitude2 - longitude1)**2 + (latitude2 - latitude1)**2)
    else:
        x1 = a1
        y1 = b1
        x2 = a2
        y2 = b2
        return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)