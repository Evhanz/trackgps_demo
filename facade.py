
#Esta libreria es para formatear los datos si son necesario
from datetime import datetime, date, time, timedelta
def funy():
    print('hola')

def getTimeLima(date):
    format = '%Y-%m-%dT%H:%M:%S%z'
    newDate = datetime.strptime(date, format)
    newDate = newDate -  timedelta(hours=5)
    newDate = newDate.strftime("%Y-%m-%d %H:%M:%S")
    return newDate