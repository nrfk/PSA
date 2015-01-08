# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: ?
"""

'''
imports et paramètres
'''
import pandas as pd
from random import *
import math
import numpy as np
import pyproj
from pyproj import proj
import mpl_toolkits.basemap.pyproj as pyproj

'''
fonctions
'''

###Définission de la fonction générant les distances
def fonctionDistance(moy,sigma):
    distance = np.random.lognormal(mu, sigma, 1)[0]
    return distance
    
##Définission de la fonction qui génère les coordonnées d'Arrivé
    
def generationVilleArrivee(latitudeDepart, longitudeDepart):
    ### Définission une projection géographique avec Proj4 la grille Icelandic grid
    isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
    ###Définission de la lat et lon en wgs84
    wgs84=pyproj.Proj("+init=EPSG:4326")
    
    ###◘Convertion de GPS en coordonnée géographique
    x,y = pyproj.transform(wgs84, isn2004, LongitudeDepart, LatitudeDepart)
    
    ###Choix uniforme d'un angle
    Angl= randint(0,360)
    ###Transformation Angle en radian
    Angle = math.radians(Angl)
    
    ##Défiistion de la distance soir rayon du cercle
    rayon = fonctionDistance(moy,sigma)
    
    ###Calcule des nouvelles coordonnées
    
    nouveau_x= x + rayon*(math.cos(Angle))
    nouveau_y= y + rayon*(math.sin(Angle))
    
    ###Convertion coordonnée géographique en coordonnée GPS
    
    LongitudeArrive, LatitudeArrive = pyproj.transform(isn2004, wgs84, nouveau_x, nouveau_y)
    
    return LongitudeArrive, LatitudeArrive 
