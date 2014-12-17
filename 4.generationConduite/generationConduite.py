# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:21:35 2014

@author: ?
"""

'''
imports et paramètres
'''
import pandas as pd

'''
fonction
'''
route = [[45, 45, 90],[65,45,130],[70, 50, 50]]
def generationConduite(route):
    trajet = pd.DataFrame(route)
    return trajet