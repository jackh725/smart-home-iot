from machine import Pin
from dht import DHT11

sensor = DHT11(Pin(15))

# while True:
#     utime.sleep(20)
#     data_dht = DHT11(pin)
#     data_dht.measure()
#     temp = data_dht.temperature()
#     humidity = data_dht.humidity()
#     print("temp is:{}".format(temp))
#     print("hum is :{}".format(humidity))

def read_dht11():
    try:
        sensor.measure()
        return sensor.temperature(), sensor.humidity()
    except:
        return -1, -1
    
#print(read_dht11())