# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:34:42 2014

@author: roms
"""

import sys
sys.path.append('/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/4.generationConduite/')

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
from fonctionRegimemoteurRapport import fonctionRegimemoteurRapport

'''
fonctions
'''

# charge tous les trajets d'un dossier
def chargeTrajets(chemin):
    trajets = pd.DataFrame()
    dt = 1/3600 # 1 frame = 1 second
    for file in range(1,201):
        try:
            trajet = pd.read_csv(chemin + '/' + str(file) + '.csv')
            trajet['conducteurId'] = chemin.split('/')[-1]
            trajet['trajetId'] = file
            trajet['vitesse'] = (trajet['x'].diff()**2 + trajet['y'].diff()**2).apply(math.sqrt)/1000/dt
            trajets = trajets.append(trajet, ignore_index = True)
        except:
            pass
    return trajets

'''
main
'''

# charge tous les chemins pour un conducteur donné
conducteur = '178'
trajets = chargeTrajets('/home/roms/Kaggle/AXA/Data/drivers/' + conducteur)

# définit les paramètres pour le calcul du rapport/régime moteur
alpha = np.array([-0.020, -0.018, -0.016, -0.014, -0.012, -0.010])
vitessesInput = np.array([20.0,35.0,55.0,75.0,90.0,110.0])
regimesInput = np.array([2000.0,2500.0,2500.0,2500.0,2500.0,2500.0])
regimeChangementrapport = [3000,3000,3000,3000,3000,9000]
vitesseMax = 200
valeursMoteur = fonctionRegimemoteurRapport(alpha, vitessesInput, regimesInput, regimeChangementrapport, vitesseMax)

# calcule le régime/rapport moteur
trajets['regime'] = valeursMoteur['regime'][trajets['vitesse'].apply(round)].values
trajets['rapport'] = valeursMoteur['rapport'][trajets['vitesse'].apply(round)].values

# quelques statistiques
plt.title('Temps pour chaque rapport de boite')
plt.xlabel('rapport')
plt.ylabel('heures')
val = trajets['rapport'].value_counts()/3600
plt.bar(val.index , val.values, align = 'center')

bins_ = range(0, 4500, 500)
plt.title('Temps pour chaque régime')
plt.xlabel('régime')
plt.ylabel('heures')
val2 = trajets['regime'][trajets['regime']>=0].values
plt.hist(val2, bins = bins_, weights = [1/3600]*len(val2))
