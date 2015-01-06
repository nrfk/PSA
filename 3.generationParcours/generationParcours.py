# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014
Last Updated on Sun Jan 05 22:57 

@author: Raoul Fokou
"""


'''
imports et paramètres
'''
from googlemaps import Client # pip install GoogleMaps, # http://py-googlemaps.sourceforge.net/, 
import pandas as pd

api_key = "AIzaSyCHm4msRkOxGwmI3qhV-gXOsAKBPcH_IoM"
routemode='driving'; routealternatives=False; routelanguage='Fr'
SavetoCsv = True

def generationParcours(latitudeDepart, longitudeDepart, latitudeArrivee, longitudeArrivee, api_key, blnSavetoCSV):
    #Output panda dataframe: #1: lng | #2: lat | #3: distance | #4: duration | #5: vitesse moyenne
    # Liste de listes. Pour chaque liste, 1er élément = latitude, 2e = longitude, 3e = vitesse max    
    # route = [[latitudeDepart, longitudeDepart, 90],[65.000,45.000,130],[latitudeArrivee, longitudeArrivee, 50]]
    googlemap = Client(api_key)
    parcours = googlemap.directions((latitudeDepart, longitudeDepart), (latitudeArrivee, longitudeArrivee), mode=routemode, alternatives=routealternatives, language=routelanguage)
    if len(parcours) > 0:
        #ErreurParcours = str(parcours[0]['summary'])
        etapes = parcours[0]['legs'][0]['steps']
        ParcoursEtapes=[]           
        for numetape in range(0, len(etapes)):
            ParcoursEtape= []
            etape = etapes[numetape]
            #print numetape, etape['start_location']['lat'], etape['start_location']['lng'], etape['end_location']['lat'], etape['end_location']['lng'], etape['distance']['value'], etape['duration']['value']
            if etape['duration']['value'] != 0:
                vitmoyms = float(etape['distance']['value'] / etape['duration']['value']) # metres par seconde
                vitmoykmh = float(3.6*vitmoyms) # kilomètre par heure
            #print numetape, vitmoyms, vitmoykmh
            ParcoursEtape.append(etape['start_location']['lat'])
            ParcoursEtape.append(etape['start_location']['lng'])
            ParcoursEtape.append(etape['distance']['value']) # eb mètres
            ParcoursEtape.append(etape['duration']['value']) # en secondes
            ParcoursEtape.append(vitmoykmh)
            ParcoursEtapes.append(ParcoursEtape)
            pd.DataFrame(ParcoursEtapes, columns=('lat', 'lng', 'distance', 'duration', 'vit.moy')).to_csv("generationParcours.csv", sep='\t', encoding='utf-8')
        return pd.DataFrame(ParcoursEtapes, columns=('lat', 'lng', 'distance', 'duration', 'vit.moy') )
    else: return False
        #if ErreurParcours.find("Channel") > 0: print 'None'# ; return 'None'
    
depart = (50.943571, 1.851318); #print googlemap.reverse_geocode(address) #'78 Rue des Fontinettes, 62100 Calais, France'  #-> lat: 50.943571,  lng: 1.851318 
destination = (43.293313, 5.371159); #print googlemap.reverse_geocode(destination) #'6-8 Rue Fort Notre Dame, 13001 Marseille' # -> lat: 43.293313, lng: 5.371159
#destination = (51.023712, 1.405465) #Manche (mer)
#destination = (40.404963, 5.628690) #Mer Méditerranée
#destination = (41.921565, 8.738669999999999) # print googlemap.geocode('Rue Jérôme Péri, 20000 Ajaccio') 

latitudeDepart = depart[0]; longitudeDepart = depart[1]
latitudeArrivee = destination[0]; longitudeArrivee = destination[1]

print generationParcours(latitudeDepart, longitudeDepart, latitudeArrivee, longitudeArrivee, api_key, SavetoCsv)
