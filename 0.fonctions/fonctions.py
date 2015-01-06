# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:22:38 2015

@author: roms
"""

import math
import utm

def toXY(longitude, latitude):
    valeur = utm.from_latlon(latitude, longitude)    
    x = valeur[0]
    y = valeur[1]
    zoneNumber = valeur[2]
    zoneLetter = valeur[3]
    return x, y, zoneNumber, zoneLetter

def toLongLat(x, y, zoneNumber, zoneLetter):
    valeur = utm.to_latlon(x, y, zoneNumber, zoneLetter)
    longitude = valeur[1]
    latitude = valeur[0]
    return longitude, latitude

def distance(a1, b1, a2, b2, type_):
    # si on a une longitude et une latitude
    if(type_ == 0):
        r = 6378.137 * 1000
        longitude1 = a1 * math.pi / 180 # radians
        latitude1 = b1 * math.pi / 180
        longitude2 = a2 * math.pi / 180
        latitude2 = b2 * math.pi / 180
        return r * math.acos(math.cos(latitude1) * math.cos(latitude2) * math.cos(longitude2 - longitude1) + math.sin(latitude1) * math.sin(latitude2))
    # si on a deux coordonnées (x, y) DE LA MÊME ZONE
    elif(type_ == 1):
        x1 = a1
        y1 = b1
        x2 = a2
        y2 = b2
        return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    else:
        return -1
