import requests
from facade import *
from repository import *

def fetchData (data):
    #se habilita que informacion es necesaria
    coorx = data.get('coorx', [])
    coory = data.get('coory', [])
    coorz = data.get('coorz', [])
    results = data.get('results',[])
    
    if results:
        for pokemon in results:
            name = pokemon['name']
            print(name)

def main():
   points =  getPoints(4 , 10,'2020-03-25', ['00:00:00','23:59:00'])
   #print(points)
   for point in points:
       position = point['position']
       velocity = point['velocity']
       print("================>")
       print(getTimeLima(point["utc"]))
       print({"altitude": position["altitude"],
            "longitude": position["longitude"],
            "latitude": position["latitude"],
            "direction":velocity["heading"]
            })
  

def mainLast():
  url = 'https://pokeapi.co/api/v2/pokemon-form'
  
  response = requests.get(url)
  if response.status_code == 200:

      data = response.json()
      print('Ahora se imprimira el resultado ====>')
      fetchData(data)
      funy()
  
  
main()