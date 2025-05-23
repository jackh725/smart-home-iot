import serial
import json
import sqlite3
import os
from datetime import datetime
import paho.mqtt.client as mqtt

from email_alert import send_alert_email


ser = serial.Serial('/dev/serial0', 9600,timeout =1)

#conn = sqlite3.connect("sensor_data.db")   #wo fu le, path issue! get the local path for the script first!

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir,"sensor_data.db")
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temp REAL,
    hum REAL,
    light INTEGER,
    distance REAL,
    alert_type TEXT
)
''')

conn.commit()
print("DB is ready")  #for debugging

print("listening on /dev/serial0....")

mqtt_client = mqtt.Client()
mqtt_client.connect("www.mqtt-dashboard.com", 1883,60)   #1883 is defualt port for mqtt, 60 is 60s

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Raw", line)
            try:
                data = json.loads(line)
                #print("Parsed:",data)
                ts = datetime.now().isoformat()  #change timestamp to iso 8601 human readable format
                temp =  data.get("temp")
                hum = data.get("hum")
                light = data.get("light")
                distance =  data.get("distance")
                alert_type = data.get("alert_type")
                #insert to sqlite
                cursor.execute('''
                    INSERT INTO sensor_data (timestamp, temp,hum,light,distance,alert_type) VALUES(?,?,?,?,?,?)
                    ''',
                    (ts,
                    temp,
                    hum,
                    light,
                    distance,
                    alert_type
                    ))
                conn.commit()
                print("data saved at ", ts)

                mqtt_payload = json.dumps({
                    "timestamp": ts,
                    "temp": temp,
                    "hum": hum,
                    "light":light,
                    "distance": distance,
                    "alert_type": alert_type
                    })
                mqtt_client.publish("home/jacktest",mqtt_payload)

                if alert_type and alert_type.lower() != "none":
                    send_alert_email(alert_type, ts, distance, light)


            except json.JSONDecodeError:
                print("Failed to parse json")
    except Exception as e:
        print("Error:", e)