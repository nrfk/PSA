# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: ?
"""

'''
imports et paramètres
'''
import pandas as pd

'''
fonction
'''
def generationRoute(latitudeDepart, longitudeDepart, latitudeArrivee, longitudeArrivee):
    # Liste de listes. Pour chaque liste, 1er élément = latitude, 2e = longitude, 3e = vitesse max    
    route = [[latitudeDepart, longitudeDepart, 90],[65.000,45.000,130],[latitudeArrivee, longitudeArrivee, 50]]
    return route