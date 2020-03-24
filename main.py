import requests
from facade import *

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
  url = 'https://pokeapi.co/api/v2/pokemon-form'
  
  response = requests.get(url)
  if response.status_code == 200:

      data = response.json()
      print('Ahora se imprimira el resultado ====>')
      fetchData(data)
      funy()
  
  
main()