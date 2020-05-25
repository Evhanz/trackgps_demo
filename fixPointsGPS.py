import requests
from facade import *
from apiRepository import *
from dbRepository import * 
from helpers import *
from datetime import datetime, date, time, timedelta

def main():
  global cantMaxValuesArray
  proccessEquipmentAllowed()

def getPointsByEquipmentApi(equipment , application, date , rangTime):
    points =  getPoints(equipment , 10,'2020-03-25', rangTime)
    response = []
    #print(points)
    for point in points:
     # print("================>")
      newPoint = getPointFormated(point, mainConfiguration)
      #print(newPoint)
      response.append(newPoint)
    return response
  

def proccessEquipmentAllowed():
    global cantMaxValuesArray #que generalmente esta en 360
    print("========= Empieza traer equipos === ")
    equipments = getAllEquipment()

    print("====== teminar :  " + getDateNow())

    for equiment in equipments:
       newEquipment = getEquipmentFormated(equiment)
       print("======== Equipo : "+ str(newEquipment['id']) +" ======== ")
       nowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


       lastDate     = getTimeStampSubCantInterval(nowDate, 2700).strftime("%Y-%m-%d %H:%M:%S")
       untilDate    = nowDate

       #obtenemos los puntos que tiene el equipo 
       # Insertar log para el inicio del proceso 
       print("======= Empieza traer API === "+ getDateNow() +"=== Last | until =>  "+lastDate+"|"+untilDate)
       pointsEquipment = getPointsByEquipmentApi(newEquipment['placa'], 10, '2020-03-25', [lastDate, untilDate])
       print("====== teminar :  " + getDateNow())
       #insertar log para el inicio dle proceso de insercion
       print("========= Empieza Insertar en BD ===> "+str(len(pointsEquipment)))
       # ----> insertPoints(newEquipment['id'], pointsEquipment)
       #insertar log para el inicio dle proceso de insercion
       print("====== temina :  " + getDateNow())

def getInitTurn():
    nowDate = datetime.now()
    response = ''

    nowHour = int(nowDate.strftime("%H"))
    if (nowHour >= 7) and (nowDate<=19):
        response = nowDate.strftime("%Y-%m-%d")
        response = response + " 07:00:00"
    else:
        if nowHour < 7:
            nowDateWithOutHour = nowDate.strftime("%Y-%m-%d") + " 19:00:00"
            response = getTimeStampSubCantlDay(nowDateWithOutHour,1)
        else:
            response = nowDate.strftime("%Y-%m-%d") + " 19:00:00"
        

    return response

main()