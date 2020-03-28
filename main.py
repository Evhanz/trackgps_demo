import requests
from facade import *
from apiRepository import *
from dbRepository import * 
from helpers import *
from datetime import datetime, date, time, timedelta

def main():
  global cantMaxValuesArray
  #getPointsByEquipmentApi(4, 10, '2020-03-25', ['00:00:00','23:59:00'])
  getEquipmentAllowed()

def getPointsByEquipmentApi(equipment , application, date , ragettime):
    points =  getPoints(4 , 10,'2020-03-25', ['00:00:00','23:59:00'])
    response = []
    #print(points)
    for point in points:
     # print("================>")
      newPoint = getPointFormated(point)
      #print(newPoint)
      response.append(newPoint)
    return response

def getEquipmentAllowed():
    global cantMaxValuesArray #que generalmente esta en 360
    equipments = getAllEquipment()

    for equiment in equipments:
       newEquipment = getEquipmentFormated(equiment)
       nowDate = datetime.now().strftime("%y-%m-%d %H:%M:%S")
       lastDate = getTimeStampAddCantInterval(newEquipment['tiem_creac'], newEquipment['cant_values'])
       #obtenemos los puntos que tiene el equipo
       pointsEquipment = getPointsByEquipmentApi(newEquipment['id'], 10, '2020-03-25', [lastDate, nowDate])
       if(len(pointsEquipment)>0):
           flagFullValues = newEquipment['cant_values'] + len(pointsEquipment)
            #evaluamos si supera el maximo de valores
           if(flagFullValues>cantMaxValuesArray): #quiere decir que exceden a la hora
               print('son mayores')
               cantValuesInsert = (cantMaxValuesArray -  newEquipment['cant_values']) # cantidad de valores para insertar normalmente
               if(cantValuesInsert>0): 
                   valuesForInsert = pointsEquipment[0:(cantValuesInsert-1)]
                   insertPoints(valuesForInsert) # se insertan los puntos
                   #================= iteramos los puntos restantes ===========
                   cantIterators = getCantIterator(len(pointsEquipment) - cantValuesInsert)
                   for i in range(cantIterators):
                       indexIni = cantValuesInsert + (cantMaxValuesArray*i)
                       indexFin = indexIni + cantMaxValuesArray - 1
                       valuesForInsert = pointsEquipment[indexIni:indexFin]
                       insertPoints(valuesForInsert)
               else: 
                   print('Exite un error de mayores de 360 valores', len(pointsEquipment))

           else:
               #se inserta normalmente
               print('Se inserta normalmente')



main()