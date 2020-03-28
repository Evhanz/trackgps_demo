import requests
def main():
  url = 'http://trackingmss.server93.com/comGpsGate/api/v.1/applications/4/tokens'
  args = {'nombre':'Eidel', 'curso':'py'}
  json = {"password": "Mss$2045", "username": "admin"}
  try:
      response = requests.post(url, json=json)
      if response.status_code == 200:
          response_json = response.json()
          print(response_json['token'])
          # origin = response_json['args']
          # print(origin['curso'])
        #  print(response_json)
        #   Tipo 1  
        #   file = open('google.html', 'wb')
        #   file.write(content)
        #   file.close()
        #   print('termino')

  except:
      print("La url no existe , o no es accesible")

def mainLast():
  url = 'https://pokeapi.co/api/v2/pokemon-form'
  
  response = requests.get(url)
  if response.status_code == 200:

      data = response.json()
      print('Ahora se imprimira el resultado ====>')
      fetchData(data)
      funy()
  
  
main()