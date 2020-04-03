from faker import Faker
from datetime import datetime, date, time, timedelta
from facade import *
import json

def main():
    data = []

    timeTemplate = "2020-02-11 09:10:00"

    fake = Faker()
    Faker.seed(0)
    for i in range(5):
        value = {
            "altitude":  float(fake.coordinate()),
            "longitude": float(fake.longitude()),
            "latitude":  float(fake.latitude()),
            "velocity":  10.0,
            "heading" : 0.0 ,
            "timeReg": getTimeStampAddCantInterval(timeTemplate, i).strftime("%Y-%m-%d %H:%M:%S"), 
            "gpsAccuracy": 2.0
            }
        data.append(value)
    print(data)

    with open('/Users/evhanz/Documents/MSS/projects/test/appSer/public/demo.json', 'w') as outfile:
        json.dump(data, outfile)
main()