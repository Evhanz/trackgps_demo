import requests
from facade import *
from apiRepository import *
from dbRepository import * 
from helpers import *
from datetime import datetime, date, time, timedelta

def main():
  global cantMaxValuesArray
  getConfigurationDB()
  #getPointsByEquipmentApi(4, 10, '2020-03-25', ['00:00:00','23:59:00'])
  proccessEquipmentAllowed()
  

def getConfigurationDB():
    global mainConfiguration
    mainConfiguration = []

    configuration = getConfiguration()
    mainConfiguration = {
        configuration[0][0] : configuration[0][1],
        configuration[1][0] : configuration[1][1],
        configuration[2][0] : configuration[2][1],
        configuration[3][0] : configuration[3][1],
        configuration[4][0] : configuration[4][1],
        configuration[5][0] : configuration[5][1],
        configuration[6][0] : configuration[6][1],   
    }

def getPointsByEquipmentApi(equipment , application, date , rangTime):
    points =  getPoints(4 , 10,'2020-03-25', rangTime)
    response = []
    #print(points)
    for point in points:
     # print("================>")
      newPoint = getPointFormated(point, mainConfiguration)
      #print(newPoint)
      response.append(newPoint)
    return response

def proccessEquipmentAllowedLast():
    global cantMaxValuesArray #que generalmente esta en 360
    equipments = getAllEquipment()

    for equiment in equipments:
       newEquipment = getEquipmentFormated(equiment)
       nowDate = datetime.now().strftime("%y-%m-%d %H:%M:%S")
       lastDate     = getTimeStampAddCantInterval(newEquipment['tiem_creac'], newEquipment['cant_values']).strftime("%Y-%m-%d %H:%M:%S")
       untilDate    = getTimeStampAddCantInterval(lastDate, newEquipment['cant_values']).strftime("%Y-%m-%d %H:%M:%S")
       #obtenemos los puntos que tiene el equipo
       pointsEquipment = getPointsByEquipmentApi(newEquipment['id'], 10, '2020-03-25', [lastDate, untilDate])
       if(len(pointsEquipment)>0):
           flagFullValues = newEquipment['cant_values'] + len(pointsEquipment)
            #evaluamos si supera el maximo de valores
           if(flagFullValues>cantMaxValuesArray): #quiere decir que exceden a la hora
               print('son mayores')
               cantValuesInsert = (cantMaxValuesArray -  newEquipment['cant_values']) # cantidad de valores para insertar normalmente
               if(cantValuesInsert>0): 
                   valuesForInsert = pointsEquipment[0:(cantValuesInsert-1)]
                   insertPoints(newEquipment['id'], valuesForInsert) # se insertan los puntos
                   #================= iteramos los puntos restantes ===========
                   cantIterators = getCantIterator(len(pointsEquipment) - cantValuesInsert)
                   for i in range(cantIterators):
                       indexIni = cantValuesInsert + (cantMaxValuesArray*i)
                       indexFin = indexIni + cantMaxValuesArray - 1
                       valuesForInsert = pointsEquipment[indexIni:indexFin]
                       insertPoints(newEquipment['id'], valuesForInsert)
               else: 
                   print('Exite un error de mayores de 360 valores', len(pointsEquipment))

           else:
               #se inserta normalmente
               print('Se inserta normalmente')
               insertPoints(newEquipment['id'], pointsEquipment)

def proccessEquipmentAllowed():
    global cantMaxValuesArray #que generalmente esta en 360
    print("========= Empieza traer equipos === ")
    equipments = getAllEquipment()

    print("====== teminar :  " + getDateNow())

    for equiment in equipments:
       newEquipment = getEquipmentFormated(equiment)
       print("======== Equipo : "+ str(newEquipment['id']) +" ======== ")
       nowDate = datetime.now().strftime("%y-%m-%d %H:%M:%S")
       lastDate     = getTimeStampAddCantInterval(newEquipment['tiem_creac'], newEquipment['cant_values']).strftime("%Y-%m-%d %H:%M:%S")
       untilDate    = getTimeStampAddCantInterval(lastDate, 2700).strftime("%Y-%m-%d %H:%M:%S")
       #obtenemos los puntos que tiene el equipo 
       # Insertar log para el inicio del proceso 
       print("======= Empieza traer API === "+ getDateNow() +"=== Last | until =>  "+lastDate+"|"+untilDate)
       pointsEquipment = getPointsByEquipmentApi(newEquipment['id'], 10, '2020-03-25', [lastDate, untilDate])
       print("====== teminar :  " + getDateNow())
       #insertar log para el inicio dle proceso de insercion
       print("========= Empieza Insertar en BD ===> "+str(len(pointsEquipment)))
       insertPoints(newEquipment['id'], pointsEquipment)
       #insertar log para el inicio dle proceso de insercion
       print("====== temina :  " + getDateNow())
               

main()