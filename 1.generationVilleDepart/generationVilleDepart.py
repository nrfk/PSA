# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: ?
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
        
    def Ret_Coord_xls(self):
        df=pd.read_excel(self.CheminFichier)
        random_ind =bisect.bisect(df['Probabilité cumulée'].dropna(),random())
        dfLongi= df['Longitude en degré'].dropna()
        dfLati = df['Latitude en degré'].dropna()
        dfNomVille = df['Nom reel'].dropna()
        return   dfLongi[random_ind] , dfLati[random_ind], dfNomVille[random_ind]
        
    def Ret_Coord_csv(self):
        df =pd.read_csv(self.CheminFichier, names=['Id','Numéro du département','Slug','Nom','Nom simple','Nom reel','Nom soundex','Nom metaphone','Code postal','Numéro de commune','Code commune','Arrondissement','Canton','','Population en 2010 en centaine','Population en 1999 en centaine','Population en 2012 en centaine','Densité en 2010','Surface / superficie','Longitude en degré','Latitude en degré','Longitude en GRD','Latitude en GRD','Longitude en DMS','Latitude en DMS','Altitude minimale','Altitude maximale'])
        SommeDensite = df['Densité en 2010'].sum()
        Probabilite = df['Densité en 2010']/SommeDensite
        ProbabiliteCumule = [Probabilite[0]]
            
        for i in range(1,len(Probabilite)):
            ProbabiliteCumule.append(ProbabiliteCumule[-1] + Probabilite [i])
            
        random_ind = bisect.bisect(ProbabiliteCumule,random())
        dfLongi= df['Longitude en degré'].dropna()
        dfLati = df['Latitude en degré'].dropna()
        dfNomVille = df['Nom reel'].dropna()
        return   dfLongi[random_ind] , dfLati[random_ind], dfNomVille[random_ind]



#Test de la classe generationVilleDepart
C = generationVilleDepart()
C.CheminFichier = 'C:\\Users\\Louarradi\\Documents\\ProjetFilRouge\\villes_france.csv'
Coordonnées =C.Ret_Coord_csv()
print(Coordonnées)