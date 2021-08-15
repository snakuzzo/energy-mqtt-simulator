import os
import paho.mqtt.client as mqtt
import time
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()

DATABASE = "./fotovoltaico.db"
MQTT_SERVER = os.getenv('MQTT_SERVER','127.0.0.1')
MQTT_PORT = os.getenv('MQTT_PORT',1883)
MQTT_KEEP_ALIVE = os.getenv('MQTT_KEEP_ALIVE',60)
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_RECONNECT_DELAY = os.getenv('MQTT_RECONNECT_DELAY',5)
SCAN_INTERVAL = os.getenv('SCAN_INTERVAL',10)
PRODUCTION_CLIENT = os.getenv('PRODUCTION_CLIENT','energyprod')
PRODUCTION_TOPIC = os.getenv('PRODUCTION_TOPIC','tele/energyprod')
PRODUCTION_LWT = os.getenv('PRODUCTION_LWT','LWT/energyprod')

def mqtt_on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected!")
    else:
        print("Bad connection Returned code=",rc)

def mqtt_connect(client,lwt):

    mqtt.Client.connected_flag=False
    mqttc = mqtt.Client(client)
    mqttc.will_set(lwt, payload='Offline', qos=0, retain=True)
    mqttc.on_connect=mqtt_on_connect
    mqttc.loop_start()
    print("Connecting to MQTT broker...")
    try:
        mqttc.connect(MQTT_SERVER, int(MQTT_PORT), int(MQTT_KEEP_ALIVE))
    except Exception as e:
        print(e)
    while not mqttc.connected_flag:
        print("Trying to reconnect in {} seconds".format(MQTT_RECONNECT_DELAY))
        time.sleep(int(MQTT_RECONNECT_DELAY))
    mqttc.publish(lwt,payload='Online', qos=0, retain=True)
    mqttc.loop_stop()    #Stop loop 
    #client.disconnect() # disconnect

    return mqttc

def sql_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_production(conn):

    print("Current Time =", time.strftime('%H:%M'))
    now = time.strftime('%H:%M')
    cur = conn.cursor()
    sql_query = "SELECT energy from fotovoltaico where start_time <= '{}' and end_time > '{}' LIMIT 1".format(now, now)
    print(sql_query)
    cur.execute(sql_query)

    row = cur.fetchone()[0]
    print(str(row))
    
    return str(row)

def main():

    conn = sql_connection(DATABASE)
    mqttcProd = mqtt_connect(PRODUCTION_CLIENT,PRODUCTION_LWT)

    mqttcProd.loop_start()
    while True:
        payload = select_production(conn)
        mqttcProd.publish(PRODUCTION_TOPIC,payload)
        time.sleep(int(SCAN_INTERVAL))
    
if __name__ == '__main__':
    main()
