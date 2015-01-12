# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 15:56:15 2015

@author: roms
"""

import pandas as pd
import numpy as np
import sys
directory = '/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/'
sys.path.append(directory + '0.fonctions')
sys.path.append(directory + '1.generationVilleDepart')
sys.path.append(directory + '2.generationVilleArrivee')
sys.path.append(directory + '3.generationParcours')
sys.path.append(directory + '4.generationConduite')
sys.path.append(directory + '5.generationBrulagesFAP')
sys.path.append(directory + '6.generationPannesFAP')

from fonctions import toXY, toLongLat, memeZone, distance
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
trajet.to_csv('/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/1.generationVilleDepart/test')

# paramètres du véhicule:
alpha = np.array([-0.020, -0.018, -0.016, -0.014, -0.012, -0.010])
vitessesInput = np.array([20.0,35.0,55.0,75.0,90.0,110.0])
regimesInput = np.array([2000.0,2500.0,2500.0,2500.0,2500.0,2500.0])
regimeChangementrapport = [3000,3000,3000,3000,3000,9000]
vitesseMax = 200
tableauRegime = fonctionRegimemoteurRapport(alpha, vitessesInput, regimesInput, regimeChangementrapport, vitesseMax)
trajet['regimeMoteur'] = tableauRegime.iloc[trajet ['vitesse'].apply(int)]['regime'].values

# 4 - on génère les brulages FAP

