import utime
import ujson
import sys
from buzzer import beep
from button import is_pressed
from ultrasonic import get_distance
from light_sensor import read_light
from dht11 import read_dht11
from machine import Pin

from machine import UART

uart = UART(1,baudrate=9600, tx = Pin(4), rx = Pin(5))

LIGHT_THRESHOLD = 20000
LIGHT_CHECK_INTERVAL = 10000 #ms
ALERT_THRESHOLD = 10  #cm if <10cm beep 3 times
DIST_CHECK_INTERVAL = 1000 # ms
DIST_DURATION = 2000   #ms
DHT_CHECK_INTERVAL = 20000  #ms



last_light_check = utime.ticks_ms()
last_dist_check = utime.ticks_ms()
last_dht_check = utime.ticks_ms()

below_alert_duration = 0
close_duration = 0

buzzer_enabled = True
prev_btn_state = 0


#default value 
temp = -1
hum = -1
light = -1
distance = -1

def send_uart_data(temp, hum,light, distance, alert_type):
    data = {
        "temp":temp,
        "hum": hum,
        "light": light,
        "distance": distance,
        "alert_type": alert_type
        }
    uart.write(ujson.dumps(data) +"\n")

while True:
    
    now = utime.ticks_ms()
    
    #button press for buzzer toggle
    current_state = is_pressed()
    if current_state == 1 and prev_btn_state ==0:
        
        buzzer_enabled = not buzzer_enabled
        print("Button State is:", "Enable" if buzzer_enabled else "Disabled")
        beep(1)  #to nofity user the btn is pressed
        utime.sleep(0.5)
    pre_btn_state = current_state
    
    #check dht11 every 20 s
    if utime.ticks_diff(now, last_dht_check)>= DHT_CHECK_INTERVAL:
        temp, hum = read_dht11()
        print("Temperature is:",temp, " Humidity is: ",hum)
        send_uart_data(temp,hum, light, distance, None)
        print("DHT11 data sent!")
        last_dht_check = now
        
    #light check every 10 s
    if utime.ticks_diff(now, last_light_check)>= LIGHT_CHECK_INTERVAL:
        light = read_light()
        print("Light Level: ", light)
        if light < LIGHT_THRESHOLD:
            print("Low Light Alert!")
            if buzzer_enabled:
                beep(1)
            send_uart_data(temp, hum, light, distance, "low_light")
            print("Light data sent!")
        last_light_check = now
    
    #check distance every 1 s
    if utime.ticks_diff(now, last_dist_check) >= DIST_CHECK_INTERVAL:
        distance = get_distance()
        print("Distance is : ", distance, "cm")
        last_dist_check = now
    
        if 0 < distance < ALERT_THRESHOLD:
            below_alert_duration += DIST_CHECK_INTERVAL
        else:
            below_alert_duration = 0
            
        if below_alert_duration >= DIST_DURATION:
            print("Too close! Alert Triggered!")
            if buzzer_enabled:
                beep(3)    
             
            else:
                print("Too close! Less than 10 cm but Buzzer disabled by button")
            send_uart_data(temp,hum,light, distance, "too_close")  
            below_alert_duration = 0
        
        
        
    #below code is to test uart can send all the sensor data correctly
#     if utime.ticks_diff(utime.ticks_ms(), last_dht_check)>= 2000:
#         temp, hum = read_dht11()
#         light = read_light()
#         distance = get_distance()
#          
#         alert_type = None
#          
#         if light< LIGHT_THRESHOLD:
#             alert_type = "light"
#         elif 0 < distance < ALERT_THRESHOLD:
#             alert_type = "too_close"
#         
#         send_uart_data(temp, hum, light, distance, alert_type)
#         last_dht_check = utime.ticks_ms()

        
utime.sleep(2)
    



