# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 14:07:28 2014

@author: roms
"""

import numpy as np
import pandas as pd

'''
à chaque rapport i correspond une courbe de régime moteur:
regimemoteur_i(vitesse) = c_i * ( exp(alpha_i * vitesse) - 1)

aplha_i est choisi et c_i est déterminé à partir d'un point donné en input

les fonctions regimemoteur = f (vitesse) et rapport = f (vitesse) sont
ensuite déterminées à partir des f_i

'''

def fonctionRegimemoteurRapport(alpha, vitessesInput, regimesInput, regimeChangementrapport, vitesseMax):
    # preparation des courbes de vitesse
    vitesses =np.array([range(vitesseMax+1)])
    # calcul des paramètres c_i
    c = np.array(regimesInput/(np.exp(alpha*vitessesInput)-1))
    # calcul des courbes de régime moteur
    regimemoteur_i = c * (np.exp(vitesses.T*alpha.T)-1)
    
    # calcul de regimoteur = f(vitesse) et de rapport = f(vitesse)
    regimemoteur = np.array([0.0]*(vitesseMax+1))
    rapport = np.array([0]*(vitesseMax+1))
    rapport_i = 1
    for vitesse in range(vitesseMax+1):
        if(regimemoteur_i[vitesse, rapport_i-1] < regimeChangementrapport[rapport_i-1]):
            regimemoteur[vitesse] = regimemoteur_i[vitesse, rapport_i-1]
            rapport[vitesse] = rapport_i
        else:
            rapport_i += 1
            regimemoteur[vitesse] = regimemoteur_i[vitesse, rapport_i-1]
            rapport[vitesse] = rapport_i
    
    return pd.DataFrame(data=np.array([regimemoteur,rapport]).T, index=range(vitesseMax+1), columns = ['regime','rapport'])

# exemples de parametres de forme de chaque rapport et points
alpha = np.array([-0.020, -0.018, -0.016, -0.014, -0.012, -0.010])
vitessesInput = np.array([20.0,35.0,55.0,75.0,90.0,110.0])
regimesInput = np.array([2000.0,2500.0,2500.0,2500.0,2500.0,2500.0])
regimeChangementrapport = [3000,3000,3000,3000,3000,9000]
vitesseMax = 200
