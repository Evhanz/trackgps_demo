
#Esta libreria es para formatear los datos si son necesario
from datetime import datetime, date, time, timedelta
import utm
interval = 10
def funy():
    print('hola')

def getTimeLima(dateInput):
    format = '%Y-%m-%dT%H:%M:%S%z'
    newDate = datetime.strptime(dateInput, format)
    newDate = newDate -  timedelta(hours=5)
    newDate = newDate.strftime("%Y-%m-%d %H:%M:%S")
    return newDate

def getTimeStampAddCantInterval(dateInput,cant_interval):
    format = '%Y-%m-%d %H:%M:%S'
    secondAdd = cant_interval * 10
    response = datetime.strptime(str(dateInput), format)
    response = response +  timedelta(seconds=secondAdd)
    return response


def getCordinateToUTM(latitude,longitude):
    utmValue = utm.from_latlon(latitude, longitude) 
    return utmValue

def getPointFormated(point):
    position = point['position']
    velocity = point['velocity']

    utmValues = getCordinateToUTM(position["latitude"], position["longitude"])

    response = {
            "time":getTimeLima(point["utc"]),
            "altitude": position["altitude"],
            "longitude": position["longitude"],
            "latitude": position["latitude"],
            "direction":velocity["heading"],
            "utm":utmValues #utmValues[0]
            }
    return response      

def getEquipmentFormated(equipment):
    response = {
        "id": equipment[0],
        "nombre": equipment[1],
        "cant_values" : equipment[3],
        "tiem_creac": equipment[4]
    }
    return response