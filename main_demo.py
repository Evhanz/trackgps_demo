import requests
def main():
  url = 'http://www.httpbin.org/get'
  args = {'nombre':'Eidel', 'curso':'py'}
  try:
      response = requests.get(url, params=args)
      if response.status_code == 200:
          response_json = response.json()
          origin = response_json['args']
          print(origin['curso'])
        #  print(response_json)
        #   Tipo 1  
        #   file = open('google.html', 'wb')
        #   file.write(content)
        #   file.close()
        #   print('termino')

  except:
      print("La url no existe , o no es accesible")
  
main()