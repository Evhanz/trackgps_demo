#!/usr/bin/python
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
        print(cur.query)
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
        latitudev.append(point['utm_x'])
        longitudv.append(point['utm_y'])

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
