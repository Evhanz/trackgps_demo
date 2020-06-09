## Pasos para instar ETL de GPS trucklog.

### Instalar dependencias del proyecto 

1. Instalar python3: 
- sudo apt-get install python3
2. Instalar pip3
- sudo apt install python3-pip
- pip3 --version  => con esto verificas si esta instalado
3. Instalar Paquetes dependientes del proyecto:
- Pip3 install utm
- pip3 install pytz
- pip3 install requests
- pip3 install psycopg2
- pip3 install Faker
4. Copia el proyecto a la caperta de destino, por ejemplo : /opt/minesense/.
5. Ejecuta la siguiente linea en consola para saber si existe comunicacion con el servidor de trackinglog:
- curl --location --request POST '190.12.73.86/json/minesense/history.php' \
--header 'Content-Type: application/json' \
--data-raw '{
                "placa":"CG_GF",
                "inicio":"2020-05-26 14:45:21",
                "final":"2020-05-26 16:15:21"
}'
6. Si recibes respuesta habilita el cron.
- crontab -e
- */5 * * * * cd /[path-del-proyecto] && sh execTrack.sh
> si es que no sale la anterior opcion usa lo siguiente:
- nano /etc/crontab
- agregar la siguiente linea al final :
- */2 *   * * *   app01   cd /opt/minesense/trackgps/ && /usr/bin/python3 main.py  > /opt/minesense/trackgps/log_app.log 