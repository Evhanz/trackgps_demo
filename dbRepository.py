#!/usr/bin/python
import psycopg2
from facade import *
from config import config
viewTrack = "equipment_tracks_gps"
mainConfiguration = {}
 
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
    values = {
        "idEquipo":idEquipo,
        "id_trabajadorv": getArrayFakeByValue(cant_values,0)
    }


    query = "select  datacamiones_tracking_update("
    query +="%(idEquipo)s::bigint,'{%(id_trabajadorv)s}'::integer[],'{%(senhalgpsv)s}'::smallint[],'{%(senhalwirelessv)s}'::smallint[],'{%(tempeje1v)s}'::smallint[],"
    query +="'{%(tempeje2v)s}'::smallint[],'{%(tempeje3v)s}'::smallint[],'{%(tempeje4v)s}'::smallint[],'{%(tempeje5v)s}'::smallint[],'{%(tempeje6v)s}'::smallint[],"
    query +="'{%(presllanta1v)s}'::smallint[],'{%(presllanta2v)s}'::smallint[],'{%(presllanta3v)s}'::smallint[],'{%(presllanta4v)s}'::smallint[],'{%(presllanta5v)s}'::smallint[],"
    query +="'{%(presllanta6v)s}'::smallint[],'{%(velocidadv)s}'::smallint[],'{%(isloadv)s}'::boolean[],'{%(tonelajev)s}'::integer[],'{%(marchav)s}'::smallint[],"
    query +="'{%(incl_rollv)s}'::smallint[],'{%(incl_pitchv)s}'::smallint[],'{%(latitudev)s}'::integer[],'{%(longitudv)s}'::integer[],'{%(xcoorv)s}'::integer[],"
    query +="'{%(ycoorv)s}'::integer[],'{%(zcoorv)s}'::integer[],'{%(precisiongpsv)s}'::integer[],'{%(tramosidsv)s}'::integer[],'{%(tiem_creacv)s}'::timestamp without time zone[],"
    query +="'{%(tiem_updatev)s}'::timestamp without time zone[],'{%(direccionv)s}'::smallint[],'{%(calidad_wirelessv)s}'::smallint[],'{%(porcentaje_combustv)s}'::smallint[],'{%(porcentaje_bateria)s}'::smallint[],"
    query +="'{%(templlanta1v)s}'::smallint[],'{%(templlanta2v)s}'::smallint[],'{%(templlanta3v)s}'::smallint[],'{%(templlanta4v)s}'::smallint[],'{%(templlanta5v)s}'::smallint[],"
    query +="'{%(templlanta6v)s}'::smallint[],'{%(bateriasensorllanta1v)s}'::smallint[],'{%(bateriasensorllanta2v)s}'::smallint[],'{%(bateriasensorllanta3v)s}'::smallint[],'{%(bateriasensorllanta4v)s}'::smallint[],"
    query +="'{%(bateriasensorllanta5v)s}'::smallint[],'{%(bateriasensorllanta6v)s}'::smallint[],'{%(segmentangle)s}'::smallint[])"




    #print (query)