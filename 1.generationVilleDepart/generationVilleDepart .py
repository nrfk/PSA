# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: Louarradi Mimoune
"""

'''
imports et paramètres
'''
import pandas as pd

from bisect import bisect
import bisect
from random import random

'''
fonction
'''
class generationVilleDepart():
  #Cette méthode utilise un fichier excel 
    def __init__(self):
        self.CheminFichier=""
        
    def Ret_Coord_csv(self):
        df =pd.read_csv(self.CheminFichier, names=['Id','Numéro du département','Slug','Nom','Nom simple','Nom reel','Nom soundex','Nom metaphone','Code postal','Numéro de commune','Code commune','Arrondissement','Canton','','Population en 2010 en centaine','Population en 1999 en centaine','Population en 2012 en centaine','Densité en 2010','Surface / superficie','Longitude en degré','Latitude en degré','Longitude en GRD','Latitude en GRD','Longitude en DMS','Latitude en DMS','Altitude minimale','Altitude maximale'])
        SommePopulation = df['Population en 2012 en centaine'].sum()
        Probabilite = df['Population en 2012 en centaine']/ SommePopulation
        
        ProbabiliteCumule = [Probabilite[0]]
        for i in range(1,len(Probabilite)):
            ProbabiliteCumule.append(ProbabiliteCumule[-1] + Probabilite [i])
            
        random_ind = bisect.bisect(ProbabiliteCumule,random())
        dfLongi= df['Longitude en degré']
        dfLati = df['Latitude en degré']
        dfNomVille = df['Nom reel']
        return   dfLongi[random_ind] , dfLati[random_ind], dfNomVille[random_ind]



#Test de la classe generationVilleDepart
#C = generationVilleDepart()
#C.CheminFichier = 'C:\\Users\\Louarradi\\Documents\\ProjetFilRouge\\villes_france.csv'
for i in range(10):
    res=[]
    C = generationVilleDepart()
    C.CheminFichier = 'villes_france.csv'
    res.append(C.Ret_Coord_csv())
    print(res)
    
