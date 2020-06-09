#!/usr/bin/python
from datetime import datetime, date, time, timedelta
import psycopg2
from facade import *
from config import config
viewTrack = "equipment_tracks_gps"
 
def connectDemo():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
         # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def executeQueryThatInsert(query=""):
    conn = None
    result = []
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result


def executeQuery(query=""):
    conn = None
    result = []
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
         # execute a statement
        cur.execute(query)
        result = cur.fetchall()
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def executeQueryWithValues(query="", values={}):
    conn = None
    result = []
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
         # execute a statement
        cur.execute(query, values)
        conn.commit()
        #print(cur.query)
        result = cur.fetchall()
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def getAllEquipment():
    global viewTrack
    query = 'select  * from '+viewTrack
    equipments = executeQuery(query)
    return equipments

def getConfiguration():
    query = "select id, valordefecto from public.ts_configuracion_equipo where id in (201,202,203,204,205,206,207) order by id asc"
    configuration = executeQuery(query)
    return configuration

def updatePositionEquipment(idEquipo,points = []):

    majorTime = '1991-09-05 00:00:00' # for example
    FMT = '%Y-%m-%d %H:%M:%S'
    selectPoint = []
    if len(points) > 0:
        for point in points:
            diference_time = datetime.strptime(majorTime, FMT) - datetime.strptime(point['time'], FMT)
            if diference_time.total_seconds() < 0:
                majorTime = point['time']
                selectPoint = point

        values = {
            "idequipo_temp":idEquipo,
            "xcoor":   selectPoint['coorxLoc'],
            "ycoor":   selectPoint['cooryLoc'],
            "zcoor" :  selectPoint['altitude'],
            "direccion" :   selectPoint['direction'],
            "latitud" :     selectPoint['latitude'],
            "longitud":     selectPoint['longitude'],
            "tonelaje":      0,
            "precisiongpstemp": selectPoint['gpsAccuracy'],
            "tiem_update_temp":  selectPoint['time']
        }

        query="select public.update_posicion_equipos( "+str(idEquipo)+" ::bigint,"+str(selectPoint['coorxLoc'])+" ::integer, "
        query+=str(selectPoint['cooryLoc'])+" ::integer, "+str(selectPoint['altitude'])+" ::integer,"
        query+= str(selectPoint['direction'])+"::integer,"+str(selectPoint['latitude'])+" ::integer, "
        query+= str(selectPoint['longitude'])+"::integer,  0::smallint,  "+str(selectPoint['gpsAccuracy'])+" ::smallint,"
        query+= "'"+selectPoint['time']+"'::timestamp without time zone)"

        executeQueryThatInsert(query)


def insertPoints(idEquipo , points = []):
    cant_values = len(points)

    id_trabajador = getArrayFakeByValue(cant_values,0)
    velocidadv = []
    xcoorv = []
    ycoorv = []
    zcoorv = []
    direccionv = []
    tiem_creacv = []
    tiem_updatev = []
    latitudev = []
    longitudv = []

    for point in points:
        velocidadv.append(point['velocity'])
        xcoorv.append( point['coorxLoc'])
        ycoorv.append( point['cooryLoc'])
        zcoorv.append( point['altitude'])
        direccionv.append(point['direction'])
        tiem_creacv.append(point['time'])
        tiem_updatev.append(point['time'])
        #latitudev.append(point['utm_x']*1000000)
        #longitudv.append(point['utm_y']*1000000)
        latitudev.append(point['latitude'])
        longitudv.append(point['longitude'])

    values = {
        "idEquipo":idEquipo,
        "id_trabajadorv":   id_trabajador,
        "velocidadv":       velocidadv,
        "xcoorv" :          xcoorv,
        "ycoorv" :          ycoorv,
        "zcoorv" :          zcoorv,
        "direccionv":       direccionv,
        "tiem_creacv":      tiem_creacv,
        "tiem_updatev":     tiem_updatev,
        "latitudev":        latitudev,
        "longitudv":        longitudv
    }

    query =  "select public.datacamiones_tracking_update_last(%(idEquipo)s ::bigint, %(id_trabajadorv)s ::  integer[],"
    query += "%(velocidadv)s :: smallint[],%(xcoorv)s :: bigint[],%(ycoorv)s :: bigint[], %(zcoorv)s :: bigint[]," 
    query += "%(direccionv)s :: smallint[],%(tiem_creacv)s :: timestamp without time zone[],%(tiem_updatev)s :: timestamp without time zone[],"
    query += "%(latitudev)s :: bigint[], %(longitudv)s :: bigint[])"
    
    res = executeQueryWithValues(query, values)
