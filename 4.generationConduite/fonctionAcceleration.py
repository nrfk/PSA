# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 15:25:30 2014

@author: roms
"""

import pandas as pd
import numpy as np

'''
acceleration = f(temps en secondes)
'''

def fonctionAcceleration(T, V, tempsMax, vitesseMax):
    # preparation du df acceleration = f(temps)
    acceleration = pd.DataFrame(data = np.array(range(tempsMax+1)), index = range(tempsMax+1), columns = ['vitesse'])
    # calcul du paramètre alpha
    alpha = -np.log(1-V/vitesseMax)/T
    # calcul de la vitesse
    acceleration = acceleration.apply(lambda x : vitesseMax * (1 - np.exp(- alpha * x)))
    return acceleration

# exemple de paramètres
vitesseMax = 250 # vitesse maximum
T = 7.5 # temps pour atteindre la vitesse V
V = 100
tempsMax = 180 # nombre de secondes maximum