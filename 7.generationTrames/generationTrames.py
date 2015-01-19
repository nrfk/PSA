# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 15:56:15 2015

@author: roms
"""

import random
import pandas as pd
import numpy as np
import math
import sys
directory = '/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/'
sys.path.append(directory + '0.fonctions')
sys.path.append(directory + '1.generationVilleDepart')
sys.path.append(directory + '2.generationVilleArrivee')
sys.path.append(directory + '3.generationParcours')
sys.path.append(directory + '4.generationConduite')
sys.path.append(directory + '5.generationBrulagesFAP')
sys.path.append(directory + '6.generationPannesFAP')

from fonctions import memeZone
from generationVilleDepart import generationVilleDepart
from generationParcours import generationParcours
from generationConduite import generationConduite
from fonctionRegimemoteurRapport import fonctionRegimemoteurRapport

# 1 - on génère la ville de départ
C = generationVilleDepart()
C.CheminFichier = directory  + '1.generationVilleDepart/villes_france.csv'
villeDepart = C.Ret_Coord_csv()

# 2 - on génère la ville d'arrivée
villeArrivee = villeDepart
while(villeDepart == villeArrivee or not(memeZone(villeDepart[0], villeDepart[1], villeArrivee[0], villeArrivee[1]))):
    villeArrivee = C.Ret_Coord_csv()

# 3 - on génère le parcours
api_key = "AIzaSyCHm4msRkOxGwmI3qhV-gXOsAKBPcH_IoM" # clé google
parcours = generationParcours(villeDepart[0], villeDepart[1], villeArrivee[0], villeArrivee[1], api_key, False)

# 4 - on génère les trames
# paramètres du véhicule:
T = 12 # temps pour atteindre la vitesse V
V = 100 
tempsMax = 200
vitesseMax = 180
fact = 1/3.6 # facteur de passage des km/h en m/sec
d_arret = 300 # distance max pour l'arrêt à la fin du trajet
limites = pd.Series([30, 50, 70, 90, 110, 130])

# trajet
trajet = generationConduite(parcours, T, V, tempsMax, vitesseMax, fact, d_arret, limites)
#trajet.to_csv('test')

# paramètres du véhicule:
alpha = np.array([-0.020, -0.018, -0.016, -0.014, -0.012, -0.010])
vitessesInput = np.array([20.0,35.0,55.0,75.0,90.0,110.0])
regimesInput = np.array([2000.0,2500.0,2500.0,2500.0,2500.0,2500.0])
regimeChangementrapport = [3000,3000,3000,3000,3000,9000]
vitesseMax = 200
tableauRegime = fonctionRegimemoteurRapport(alpha, vitessesInput, regimesInput, regimeChangementrapport, vitesseMax)
trajet['regimeMoteur'] = tableauRegime.iloc[trajet ['vitesse'].apply(int)]['regime'].values
trajet['distance'] = (trajet['x'].diff()**2 + trajet['y'].diff()**2).apply(math.sqrt).cumsum()
trajet['distance'].fillna(0, inplace = True)

# 4 - on génère les brulages FAP
# paramètres du brulage
distance_avant_brulage = 4 * 1000 # distance entre deux brulages en mètres
distance_avant_panne = 2.5 * 1000 # une fois possibilité de brulage, distance max avant panne
vitesseMin_brulage = 30 # vitesse minimum pour un brulage
regimeMin_brulage = 2800 # régime minimum pour avoir un brûlage
tempsMin_brulage = 2 * 60 # durée minimum à la condition de régime en secondes

# 1ere condition: rester au-dessus d'un régime moteur donné pendant un temps minimum
conditionBrulage1 = pd.stats.moments.rolling_sum(trajet['regimeMoteur'] >= regimeMin_brulage, window = tempsMin_brulage)
conditionBrulage1.fillna(0, inplace = True)
conditionBrulage1 = (conditionBrulage1 == tempsMin_brulage) # quand Vrai, signifie que la condition 1 est remplie

# 2eme condition: être au-dessus d'une vitesse minimum au moment du brulage
conditionBrulage2 = trajet['vitesse'] >= vitesseMin_brulage

# 3eme condition: être dans la fenêtre [distance avant brûlage ; distance avant brûlage + distance avant panne]
conditionBrulage3 = trajet['distance'] % (distance_avant_brulage + distance_avant_panne)
conditionBrulage3 = (conditionBrulage3 >= distance_avant_brulage) & (distance_avant_brulage <= distance_avant_brulage + distance_avant_panne)

# une etape = un intervalle de longueur (distance_avant_brulage + distance_avant_panne])
trajet['etape'] = trajet['distance'] // (distance_avant_brulage + distance_avant_panne)

# rajout des brulage
trajet['brulage'] = 0
trajet['brulage'][conditionBrulage1 & conditionBrulage2 & conditionBrulage3] = 1

# on tire au hasard des pannes selon une loi uniforme (pas de panne si brûlage avant)
trajet['panne'] = 0
nombrePannes = int(max(trajet['distance']) // (distance_avant_brulage + distance_avant_panne) + 1)
pannes = []
for numero_panne, panne in enumerate(range(nombrePannes)):
    distancePanne = (distance_avant_brulage + distance_avant_panne) * numero_panne + random.uniform(distance_avant_brulage, distance_avant_brulage + distance_avant_panne)
    pannes.append(distancePanne)
    if distancePanne < max(trajet['distance']):
        indexPanne = min(trajet['distance'][trajet['distance'] > distancePanne].index)
        # si pas de brûlage avant l'apparition de la panne:        
        debutEtape = min(trajet[trajet['etape'] == numero_panne].index)
        if(sum(trajet['brulage'][debutEtape:(indexPanne+1)]) == 0):
            trajet['panne'].iloc[indexPanne] = 1        

# affiche le nombre de pannes + sauve résultats
print('Nombre de pannes: ' + str(sum(trajet['panne'] == 1)))
trajet.to_csv(directory + '7.generationTrames/trajet.csv', index = False)
