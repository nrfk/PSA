# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 15:56:15 2015

@author: roms
"""

###############################################################################
# IMPORTS ET FONCTIONS

import random
import pandas as pd
import numpy as np
import math
import sys
import time
directory = '/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/'
sys.path.append(directory + '0.fonctions')
sys.path.append(directory + '1.generationVilleDepart')
sys.path.append(directory + '2.generationVilleArrivee')
sys.path.append(directory + '3.generationParcours')
sys.path.append(directory + '4.generationConduite')
sys.path.append(directory + '5.generationBrulagesFAP')
sys.path.append(directory + '6.generationPannesFAP')
sys.path.append(directory + '7.generationTrames')

from fonctions import memeZone
from generationVilleDepart import generationVilleDepart
from generationParcours import generationParcours
from generationConduite import generationConduite
from fonctionRegimemoteurRapport import fonctionRegimemoteurRapport

###############################################################################
# PARAMETRES

# paramètres du véhicule:
T = 12 # temps pour atteindre la vitesse V
V = 100 
tempsMax = 200
vitesseMax = 200
fact = 1/3.6 # facteur de passage des km/h en m/sec
d_arret = 300 # distance max pour l'arrêt à la fin du trajet
limites = pd.Series([30, 50, 70, 90, 110, 130])

alpha = np.array([-0.020, -0.018, -0.016, -0.014, -0.012, -0.010]) # paramètres du modèle exponentiel de régime
vitessesInput = np.array([20.0,35.0,55.0,75.0,90.0,110.0]) # exemples de vitesses pour les rapports de boite
regimesInput = np.array([2000.0,2500.0,2500.0,2500.0,2500.0,2500.0]) # exemple de régime pour les rapports de boite
regimeChangementrapport = [3000,3000,3000,3000,3000,9000]

# paramètres pour le parcours
api_key = "AIzaSyCHm4msRkOxGwmI3qhV-gXOsAKBPcH_IoM" # clé google
numeroParcours = 0 # numéro assigné au premier parcours-1
distanceParcourue = 0

# paramètres du brulage
distance_avant_brulage = 4 * 1000 # distance entre deux brulages en mètres
distance_avant_panne = 2.5 * 1000 # une fois possibilité de brulage, distance max avant panne
vitesseMin_brulage = 30 # vitesse minimum pour un brulage
regimeMin_brulage = 2800 # régime minimum pour avoir un brûlage
tempsMin_brulage = 2 * 60 # durée minimum à la condition de régime en secondes

# distance à parcourir pour ce véhicule (attention, en METRES!)
distanceAParcourir = 1500 * 1000

###############################################################################
# ALGORITHME DE GENERATIOND DE TRAJETS

start_time = time.time()
while(distanceParcourue < distanceAParcourir):
    # 1 - on génère la ville de départ et d'arrivée
    numeroParcours += 1 
    if(numeroParcours == 1):
        # cas du premier parcours: on choisit une ville de départ au hasard
        C = generationVilleDepart()
        C.CheminFichier = directory  + '1.generationVilleDepart/villes_france.csv'
        villeDepart = C.Ret_Coord_csv()
        villeArrivee = villeDepart # seulement pour avoir le même type de données
        while(villeDepart == villeArrivee or not(memeZone(villeDepart[0], villeDepart[1], villeArrivee[0], villeArrivee[1]))):
            villeArrivee = C.Ret_Coord_csv()
    else:
        # sinon on choisit la dernière ville d'arrivée
        villeDepart = villeArrivee
        while(villeDepart == villeArrivee or not(memeZone(villeDepart[0], villeDepart[1], villeArrivee[0], villeArrivee[1]))):
            villeArrivee = C.Ret_Coord_csv()
    
    # 2 - on génère le parcours
    parcours = generationParcours(villeDepart[0], villeDepart[1], villeArrivee[0], villeArrivee[1], api_key, False)
    
    # 3 - on génère le trajet
    trajet = generationConduite(parcours, T, V, tempsMax, vitesseMax, fact, d_arret, limites)
    tableauRegime = fonctionRegimemoteurRapport(alpha, vitessesInput, regimesInput, regimeChangementrapport, vitesseMax)
    trajet['regimeMoteur'] = tableauRegime.iloc[trajet ['vitesse'].apply(int)]['regime'].values
    trajet['distance'] = (trajet['x'].diff()**2 + trajet['y'].diff()**2).apply(math.sqrt).cumsum()
    trajet['distance'].fillna(0, inplace = True)
    
    # 5 - on génère les brulages FAP
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
    
    # on rajoute le numéro du parcours
    trajet['numeroParcours'] = numeroParcours
    
    # on rajoute le trajet au df de tous les trajets ainsi que la distance totale
    if(numeroParcours == 1):
        # cas du premier parcours: on crée un DF pour tous les trajets
        trajets = trajet.copy()
        distanceParcourue += max(trajet['distance'])
    else:
        trajet['distance'].apply(lambda x: x + distanceParcourue) # ajoute la distance parcourue au trajet précédent
        distanceParcourue += max(trajet['distance']) # ajoute à ce total la distance poarcourue au trajet en cours
        trajets = trajets.append(trajet, ignore_index = True)

# runtime of the algorithm:
print(str(round(time.time() - start_time)) + " seconds to generate " + str(round(distanceParcourue/1000.0)) + ' kilometers')

'''
trajets.shape

sum(trajets['panne'])

trajets.to_csv('/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/7.generationTrames/trajets.csv')

from matplotlib import pyplot as plt
plt.plot(trajets['numeroParcours'])

plt.plot(trajets['x'], trajets['y'])
'''