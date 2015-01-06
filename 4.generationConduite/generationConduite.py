# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: ?
"""

'''
imports et paramètres
'''

import sys
sys.path.append('/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/4.generationConduite/')

import pandas as pd
import numpy as np
from fonctionDeceleration import fonctionDeceleration
from fonctionAcceleration import fonctionAcceleration

'''
fonction
'''
def generationConduite(route, T, V, tempsMax, vitesseMax, fact, d_arret, limites):
    # ajoute les limitates de vitesse dans le DF
    route['vitesse'] = route['distance'] / route['duration'] * 3.6
    route['vitesse_limite'] = route['vitesse'].apply(lambda x : min(x, max(limites)))
    route['vitesse_limite'] = route['vitesse_limite'].apply(lambda x : min(limites[(limites >= x)]))
    # ajoute les coordonnées (x, y) en mètres
    route['x'] = route['lng'] * 111111 # A COMPLETER !!!
    route['y'] = route['lat'] * 111111 # A COMPLETER !!!
    # extrait les infos nécessaires
    route = np.array(route[['x', 'y', 'vitesse_limite']])    
    
    route[-1, -1] = 0 # change la dernière limite de vitesse pour l'arrêt
    alpha = (route[-1, 1] - route[-2, 1]) / (route[-1, 0] - route[-2, 0])
    x_arret = route[-1, 0] + np.sign(route[-1, 0] - route[-2, 0]) * np.sqrt(d_arret**2 / (alpha**2 + 1))
    y_arret = route[-1, 1] + np.sign(route[-1, 1] - route[-2, 1]) * np.sqrt(d_arret**2 / (1/alpha**2 + 1))
    route = np.vstack([route, [x_arret, y_arret, 0]]) # ajoute un dernier point à +50 mètres (arrêt)
    
    # initialisation
    dt = 1
    x_i = route[:, 0]
    y_i = route[:, 1]
    v_aut_i = route[:, 2]
    d_i = np.append([0.0], np.sqrt(np.diff(x_i)**2 + np.diff(y_i)**2))
    d_i_cum = np.cumsum(d_i)
    
    t = [0]
    d = [0.0]
    u = 0.0
    theta = 0.0
    v_aut = [float(v_aut_i[0])]
    v = [0.001] # différent de 0 pour partir dans la boucle
    t_acc = 0
    t_dec = 0
    i = [0]
    x = [float(x_i[0])]
    y = [float(y_i[0])]
    
    # charge le modèle d'accélération
    acceleration = fonctionAcceleration(T, V, tempsMax, vitesseMax)
    deceleration = fonctionDeceleration(vitesseMax, -50)
    
    # on calcule les différents points
    while(v[-1] > 0):
        # rajoute une seconde
        t.append(t[-1]+1)
    
        # calcul de la nouvelle vitesse
        if(v_aut[-1] > v[-1]):
            # accélération
            t_acc += 1
            t_dec = 0
            v.append(acceleration['vitesse'][t_acc])
        elif(v_aut[-1] < v[-1]):
            # si première décélératon ou changement de vitesse autorisée chargement du modèle
            if(t_dec == 0 or v_aut[-1] != v_aut[-2]):
                # coef de décélération (nombre de km/h perdus par seconde)
                coef = min(-1, max(-10, -(v[-1]-v_aut[-1])/4))
                deceleration = fonctionDeceleration(v[-1], coef)
            t_dec += 1
            v.append(deceleration['vitesse'][t_dec])
            # on recalcule le temps d'accélération comme le temps correspondant à la
            # vitesse immédiatement supérieure à la nouvelle vitesse calculée
            t_acc = min(acceleration['vitesse'][acceleration['vitesse'] > v[-1]].index) - 1
        else:
            # on maintient la vitesse
            v.append(v[-1])
            t_dec = 0
            
        # on en déduit la distance parcourue et l'étape
        d.append((v[-1]+v[-2]) / 2 * dt * fact)
        i.append(sum(sum(d) >= d_i_cum) -1)
        
        # en cas de changement d'étape
        if(i[-1] != i[-2]):
            u = sum(d) - sum(d_i[:i[-1]+1])
            theta = np.arctan((y_i[i[-1] + 1] - y_i[i[-1]]) / (x_i[i[-1] + 1] - x_i[i[-1]]))
            if((x_i[i[-1] + 1] - x_i[i[-1]]) < 0):
                theta = np.pi + theta
            v_aut.append(v_aut_i[i[-1]])
            x.append(x_i[i[-1]] + u * np.cos(theta))
            y.append(y_i[i[-1]] + u * np.sin(theta))
        else:
            u = d[-1]
            theta = np.arctan((y_i[i[-1] + 1] - y_i[i[-1]]) / (x_i[i[-1] + 1] - x_i[i[-1]]))
            if((x_i[i[-1] + 1] - x_i[i[-1]]) < 0):
                theta = np.pi + theta
            v_aut.append(v_aut[-1])
            x.append(x[-1] + u * np.cos(theta))
            y.append(y[-1] + u * np.sin(theta))
    
    trajet = pd.DataFrame(data = np.array((x, y)).T, index = t, columns = ['x', 'y'])
    return trajet

# exemple:
T = 12 # temps pour atteindre la vitesse V
V = 100 
tempsMax = 200
vitesseMax = 180
fact = 1/3.6 # facteur de passage des km/h en m/sec
d_arret = 300 # distance max pour l'arrêt à la fin du trajet
# format: [x en mètres, y en mètres, v en kilomètres/h]
#route = np.array([[1, 100, 90],[100,100,130],[100, 200, 50],[150, 200, 50],[100, -50, 50]])

# charge le chemin
route = pd.DataFrame.from_csv('/home/roms/Desktop/Projet fil rouge/Scripts/GitHub/PSA/3.generationParcours/SampleOuputStage3.csv', sep = '\t')
limites = pd.Series([30, 50, 70, 90, 110, 130])

trajet = generationConduite(route, T, V, tempsMax, vitesseMax, fact, d_arret, limites)

'''
# pour debugging
from matplotlib import pyplot as plt

print('t: ' + str(t[-1]))
print('t_dec: ' + str(t_dec))
print('t_acc: ' + str(t_acc))
print('d: ' + str(d[-1]))
print('i: ' + str(i[-1]))
print('u: ' + str(u))
print('theta: ' + str(theta))
print('v: ' + str(v[-1]))
print('v_aut: ' + str(v_aut[-1]))
print('x: ' + str(x[-1]))
print('y: ' + str(y[-1]))
print('---------------------------')

# pour debugging
plt.figure(figsize = (10, 5))
fig, ax1 = plt.subplots(figsize = (10, 5))
plt.xlim(min(min(x_i[:len(x_i)-1]),min(x))-50, max(max(x_i[:len(x_i)-1]),max(x))+50)
plt.ylim(min(min(y_i[:len(y_i)-1]),min(y))-50, max(max(y_i[:len(y_i)-1]),max(y))+50)
ax1.plot(x_i[:len(x_i)-1], y_i[:len(y_i)-1], 'o')
ax1.plot(x, y, 'b+')
ax1.set_xlabel('distance x')
ax1.set_ylabel('distance y', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax2 = ax1.twinx()
ax2.plot(x, v, 'g-')
ax2.plot(x, v_aut, 'r-')
ax2.set_ylabel('vitesse + vitesse autorisée en rouge', color='g')
for tl in ax2.get_yticklabels():
    tl.set_color('g')
plt.show()

# on recalcule la vitesse pour vérification
import math
vitesse_effective = (trajet['x'].diff()**2 + trajet['y'].diff()**2).apply(math.sqrt)/fact
plt.plot(vitesse_effective, 'b')
plt.plot(v, 'g')
plt.plot(vitesse_effective-v, 'r')
'''
