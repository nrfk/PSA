# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 15:25:30 2014

@author: roms
"""

import pandas as pd
import numpy as np

'''
deceleration = f(temps en secondes)

paramètres:
- vMax (la vitesse max du véhicule)
- coef (entre -1 et -50, le nombre de km/h que l'on perd par seconde)
'''
def fonctionDeceleration(V0, coef):
    # preparation du df deceleration = f(temps)
    n = int(np.ceil(- V0 / coef))
    deceleration = pd.DataFrame(data = np.array(range(n+1)) + 0.0, index = range(n+1), columns = ['vitesse'])
    # calcul de la vitesse
    deceleration = deceleration.apply(lambda x : np.maximum( 0 , V0 + coef * x ))
    return deceleration

# exemple de paramètres
V0 = 200
coef = -50 # correspond à un freinage d'urgence