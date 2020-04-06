#!/usr/bin/python
from datetime import datetime, date, time, timedelta
cantMaxValuesArray = 360

def getCantIterator(value):
    global cantMaxValuesArray
    cant = value // cantMaxValuesArray
    if(value%cantMaxValuesArray >0): 
        cant = cant + 1
    #print(cant, value)
    return cant

def getDateNow():
    response = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    return response