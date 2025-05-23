import serial
import json

ser = serial.Serial('/dev/serial0', 9600,timeout =1)

print("listening on /dev/serial0....")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Raw", line)
            try:
                data = json.loads(line)
                print("Parsed:",data)
            except josn.JSONDecodeError:
                print("Failed to parse json")
    except Exception as e:
        print("Error reading UART:", e)