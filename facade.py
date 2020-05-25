
#Esta libreria es para formatear los datos si son necesario
from datetime import datetime, date, time, timedelta
from math import sin , cos
import utm
interval = 2
mainConfiguration = {}
def funy():
    print('hola')

def getTimeLima(dateInput):
    format = '%Y-%m-%dT%H:%M:%S%z'
    newDate = datetime.strptime(dateInput, format)
    newDate = newDate -  timedelta(hours=5)
    newDate = newDate.strftime("%Y-%m-%d %H:%M:%S")
    return newDate

def getTimeStampAddCantInterval(dateInput,cant_interval):
    global interval
    format = '%Y-%m-%d %H:%M:%S'
    secondAdd = cant_interval * interval
    response = datetime.strptime(str(dateInput), format)
    response = response +  timedelta(seconds=secondAdd)
    return response

def getTimeStampSubCantInterval(dateInput,cant_interval):
    global interval
    format = '%Y-%m-%d %H:%M:%S'
    secondAdd = cant_interval * interval
    response = datetime.strptime(str(dateInput), format)
    response = response -  timedelta(seconds=secondAdd)
    return response

def getTimeStampSubCantlDay(dateInput,daysIn):
    format = '%Y-%m-%d %H:%M:%S'
    response = datetime.strptime(str(dateInput), format)
    response = response -  timedelta(days=daysIn)
    return response

def getCordinateToUTM(latitude,longitude):
    utmValue = utm.from_latlon(latitude, longitude) 
    return utmValue

def getPointFormatedLast(point):
    #global mainConfiguration
    position = point['position']
    velocity = point['velocity']

    utmValues = getCordinateToUTM(position["latitude"], position["longitude"])
    localValues = getUTMtoLocal(utmValues[0], utmValues[1], mainConfiguration)

    response = {
            "time":point["utc"],
            "altitude": position["altitude"],
            "longitude": position["longitude"],
            "latitude": position["latitude"],
            "direction":velocity["heading"],
            "velocity":velocity["velocity"],
            "utm_x":utmValues[0], #utmValues[0],
            "utm_y":utmValues[1],
            "coorxLoc": localValues['coorxLoc'],
            "cooryLoc": localValues['cooryLoc']
            }
    return response 

def getPointFormated(point, configuration):
    utmValues = getCordinateToUTM(float(point["latitude"]), float(point["longitude"]))
    localValues = getUTMtoLocal(utmValues[0], utmValues[1], configuration)

    response = {
            "time":point["timeReg"],
            "altitude":     float(point["altitude"]),
            "longitude":    float(point["longitude"]),
            "latitude":     float(point["latitude"]),
            "direction":    float(point["heading"]),
            "velocity":     float(point["velocity"]),
            "utm_x":        utmValues[0], #utmValues[0],
            "utm_y":        utmValues[1],
            "coorxLoc":     localValues['coorxLoc'],
            "cooryLoc":     localValues['cooryLoc']
            }
    return response      

def getEquipmentFormated(equipment):
    response = {
        "id": equipment[0],
        "nombre": equipment[1],
        "cant_values" : equipment[3],
        "tiem_creac": equipment[4],
        "placa":equipment[5]
    }
    return response

def getArrayFakeByValue(cant, value):
    response = []
    for i in range(cant):
        response.append(value)
    return response

def getUTMtoLocal(xcoorlong, ycoorlong, configuration):

    xlf =float(configuration[201])
    ylf =float(configuration[202])
    xwf =float(configuration[203])
    ywf =float(configuration[204])
    rot =float(configuration[205])
    FUtmLoc =float(configuration[206])
    FlocUtm =float(configuration[207])

    coorxLoc = (xlf + ((xcoorlong - xwf)*(cos(rot)) - (ycoorlong- ywf)*sin(rot))*FUtmLoc)
    cooryLoc = (ylf + ((ycoorlong - ywf)*(cos(rot)) - (xcoorlong- ywf)*sin(rot))*FUtmLoc)

    return { 'coorxLoc': coorxLoc , 'cooryLoc':cooryLoc}

           

