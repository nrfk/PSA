# -*- coding: utf-8 -*-
"""
To Do: indication •1 of googlemap roadmap à finaliser
Created on Wed Dec 17 15:21:35 2014
Last Updated on Sun Jan 04 08:49 

@author: Raoul Fokou
"""


'''
imports et paramètres
'''
from googlemaps import Client 
    # http://http://py-googlemaps.sourceforge.net/
    # pip install GoogleMaps
import pandas as pd

'''
fonction
'''
#def generationRoute(latitudeDepart, longitudeDepart, latitudeArrivee, longitudeArrivee):
#    # Liste de listes. Pour chaque liste, 1er élément = latitude, 2e = longitude, 3e = vitesse max    
#    route = [[latitudeDepart, longitudeDepart, 90],[65.000,45.000,130],[latitudeArrivee, longitudeArrivee, 50]]
#    return route
    
# -*- coding: utf-8 -*-

#Output Array of list:
    #0: step
    #1: lat
    #2: long
    #3: distance
    #4: duration

def InstructiontoGPSlat(subInstruction):
    flag0 = subInstruction.find(MarkOpen)
    flag1 = subInstruction.find(MarkValue, flag0)
    flag2 = subInstruction.find(MarkComma, flag1)  
    Lat = float(subInstruction[flag1+1:flag2])
    #flag3 = subInstruction.find(MarkValue, flag2)
    #flag4 = subInstruction.find(MarkClose, flag3)
    #Lng = float(subInstruction[flag3+1:flag4])
    return Lat
def InstructiontoGPSlng(subInstruction):
    flag0 = subInstruction.find(MarkOpen)
    flag1 = subInstruction.find(MarkValue, flag0)
    flag2 = subInstruction.find(MarkComma, flag1)  
    #Lat = float(subInstruction[flag1+1:flag2])
    flag3 = subInstruction.find(MarkValue, flag2)
    flag4 = subInstruction.find(MarkClose, flag3)
    Lng = float(subInstruction[flag3+1:flag4])
    return Lng
    
def InstructiontoDuration(subInstruction):
    flag0 = subInstruction.find(MarkOpen)
    flag1 = subInstruction.find(MarkValue, flag0)
    flag2 = subInstruction.find(MarkComma, flag1)  
    flag3 = subInstruction.find(MarkValue, flag2)
    flag4 = subInstruction.find(MarkClose, flag3)
    duration = float(subInstruction[flag3+1:flag4])
    return duration # en secondes

def InstructiontoDistance(subInstruction):
    flag0 = subInstruction.find(MarkOpen)
    flag1 = subInstruction.find(MarkValue, flag0)
    flag2 = subInstruction.find(MarkComma, flag1)  
    flag3 = subInstruction.find(MarkValue, flag2)
    flag4 = subInstruction.find(MarkClose, flag3)
    distance = float(subInstruction[flag3+1:flag4])
    return distance # en mètres

MarkComma = ","
MarkValue = ':'
MarkOpen = '{'; MarkClose = '}'
api_key="AIzaSyCHm4msRkOxGwmI3qhV-gXOsAKBPcH_IoM"
KeySplit = 'travel_mode'
str_start_location = 'start_location'.encode('utf-8')
str_duration = 'duration'.encode('utf-8')
str_end_location = 'end_location'.encode('utf-8') 
str_distance = 'distance'.encode('utf-8')
KeyEnd = MarkClose.encode('utf-8')

finaloutput = []
gmaps = Client(api_key)
#Tests si adresse avec noms
address = '78 Rue des Fontinettes, 62100 Calais, France'  #-> lat: 50.943571, lng: 1.851318
print gmaps.geocode(address)
destination = '6-8 Rue Fort Notre Dame, 13001 Marseille' # -> lat: 43.293313, lng: 5.371159
print gmaps.geocode(destination)

#Tests si adresse en mode GPS
address = (50.943571, 1.851318)
print gmaps.reverse_geocode(address)
destination = (43.293313, 5.371159)
print gmaps.reverse_geocode(destination)

RoadMap= gmaps.directions(address, destination, mode='driving', alternatives=False, language='Fr')
RoadMap = str(RoadMap)
Instructions = RoadMap.split(KeySplit.encode('utf-8'))
#ToDo: 1 instruction proper handly
# Marks: Typical instruction is a combination of locations, duration, distance
    #u'start_location': {u'lat': 48.3880933, u'lng': -4.4875513}
    #u'duration': {u'text': u'1 minute', u'value': 51},
    #u'end_location': {u'lat': 48.3896599, u'lng': -4.4903794}}, 
    #{u'html_instructions': u'Au rond-point, prendre la <b>1re</b> sortie sur <b>Rue Duquesne</b><div style="font-size:0.9em">Traverser le rond-point</div>',
    #u'distance': {u'text': u'0,2 km', u'value': 249}
for step in range(1,len(Instructions)-1):#ToDo: 1 instruction cas particulier pour 1ere instruction
    output = []
    Instruction = Instructions[step]
    start_startlocation = Instruction.find(str_start_location);    end_startlocation = Instruction.find(KeyEnd, start_startlocation);
    start_distance =  Instruction.find(str_distance); end_distance =  Instruction.find(KeyEnd, start_distance)
    start_duration =  Instruction.find(str_duration);  end_duration =  Instruction.find(KeyEnd, start_duration)
    start_endlocation =  Instruction.find(str_end_location);   end_endlocation =  Instruction.find(KeyEnd, start_endlocation)  
  
    #print step, Instruction[start_startlocation:end_startlocation+1] #,start_startlocation, end_startlocation
    #print step, Instruction[start_duration:end_duration+1]
    #print step, Instruction[start_endlocation:end_endlocation+1]
    #print step, Instruction[start_distance:end_distance+1]
    #Output Array of list:
    output.append(step) #0: step
    output.append(InstructiontoGPSlat(Instruction[start_startlocation:end_startlocation+1])) #lat
    output.append(InstructiontoGPSlng(Instruction[start_startlocation:end_startlocation+1])) #long
    output.append(InstructiontoDistance(Instruction[start_distance:end_distance+1])) #distance
    output.append(InstructiontoDuration(Instruction[start_duration:end_duration+1])) #duration

    finaloutput.append(output)
df = pd.DataFrame(finaloutput, columns=('Step', 'lat', 'lng', 'distance', 'duration') )
print address, df.to_csv(index=False, header=True), destination
df.to_csv("SampleOuputStage3.tsv", sep='\t', encoding='utf-8')