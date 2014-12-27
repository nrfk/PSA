# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 15:25:30 2014

@author: roms
"""

import pandas as pd
import numpy as np

'''
deceleration = f(temps en secondes)
'''

def fonctionDeceleration(T, V0, tempsMax):
    # preparation du df deceleration = f(temps)
    deceleration = pd.DataFrame(data = np.array(range(tempsMax+1)), index = range(tempsMax+1), columns = ['vitesse'])
    # calcul de la vitesse
    deceleration = deceleration.apply(lambda x : np.maximum( 0 , V0 * (1 - x / T)))
    return deceleration

# exemple de paramètres
T = 12 # temps pour s'arrêter depuis V0
V0 = 100
tempsMax = 180 # nombre de secondes maximum
