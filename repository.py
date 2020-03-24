#Esta libreria se encarga de traer la data
import time
import requests

#variables globales
server = "http://trackingmss.server93.com/comGpsGate/api/v.1"


def getToken(idAplication = 4):
    global server
    url = "{server}/applications/{idAplication}/tokens"
    json = {"password": "Mss$2045", "username": "admin"}
    token = ""
    try:
        response = requests.post(url, json=json)
        if response.status_code == 200:
            response_json = response.json()
            token = response_json['token']
    except:
            print("La url no existe , o no es accesible")
    return token


def getPoints(idAplication = 4 , idDevice = 10, fecha = None, timeRange = []):
    #la comuniacion es por get : revisar la documentacion
    dateNow = time.strftime("%d/%m/%y")
    data = []

    if fecha is None:
        fecha = dateNow
    if len(timeRange) !=2:
        timeRange[0]=   

    apiGetPoints = "/applications/{idAplication}/users/{idDevice}/tracks?Date={fecha}&From={timeRange[0]}&Until={timeRange[1]}Filtered=true"
    token = getToken();

    response = requests.get(apiGetPoints,headers={"Authorization": token})
    if response.status_code == 200:
        data = response.json()

    return data
            