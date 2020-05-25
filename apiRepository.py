#Esta libreria se encarga de traer la data
from datetime import datetime, date, time, timedelta
import calendar
import requests

#variables globales
server = "http://190.12.73.86"


def getToken(idAplication = 4):
    global server
    url = server+"/applications/"+str(idAplication)+"/tokens"
    json = {"password": "Mss$2045", "username": "admin"} #demo
    token = ""
    response = requests.post(url, json=json)
    if response.status_code == 200:
        response_json = response.json()
        token = response_json['token']
    return token


def getPointsLast(idAplication = 4 , idDevice = 10, fecha = None, timeRange = []):
    #la comuniacion es por get : revisar la documentacion
    global server
    dateNow = datetime.now().strftime("%y/%m/%d")
    data = []
    
    if fecha is None:
        fecha = dateNow
    if len(timeRange) !=2:
        timeRange[0]=   datetime.now() -  timedelta(hours=1)
        timeRange[0] = timeRange[0].strftime("%H:%M:%S")
        timeRange[1]=   datetime.now()
        timeRange[1] = timeRange[0].strftime("%H:%M:%S")

    params = {"Date":fecha, "From":timeRange[0], "Until": timeRange[1], "Filtered":"true"}

    apiGetPoints = server+"/applications/"+str(idAplication)+"/users/"+str(idDevice)+"/tracks"
    token = getToken();

    print(apiGetPoints)
    response = requests.get(apiGetPoints,headers={"Authorization": token}, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()

    return data


def getPoints(placa = "", idDevice = 10, fecha = None, timeRange = []):
    #la comuniacion es por get : revisar la documentacion
    global server
    data = []
    
    params = {"placa":placa, "inicio":timeRange[0], "final": timeRange[1]}

    apiGetPoints = server+"/json/minesense/history.php"
    #token = getToken();

    print(apiGetPoints)
    response = requests.post(apiGetPoints, json=params)
    print(response)
    if response.status_code == 200:
        data = response.json()

    return data
            