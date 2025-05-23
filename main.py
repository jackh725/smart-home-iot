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
ALERT_THRESHOLD = 10  #cm if <10cm beep 3 times
DIST_CHECK_INTERVAL = 1000 # ms
DIST_DURATION = 5   #s

last_light_check = utime.ticks_ms()
last_dist_check = utime.ticks_ms()
last_dht_check = utime.ticks_ms()

below_alert_duration = 0
close_duration = 0

buzzer_enabled = True
prev_btn_state = 0

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
    #btn test is ok, now turn on and off
    
    current_state = is_pressed()
    if current_state == 1 and prev_btn_state ==0:
        
        buzzer_enabled = not buzzer_enabled
        print("Button State is:", "Enable" if buzzer_enabled else "Disabled")
        beep(1)  #to nofity user the btn is pressed
        utime.sleep(0.5)
    
    #light check every 10 s
    if utime.ticks_diff(utime.ticks_ms(), last_light_check)>= 10000:
        light = read_light()
        print("Light Level: ", light)
        if light < LIGHT_THRESHOLD:
            print("Low Light Alert!")
            beep(1)
        last_light_check = utime.ticks_ms() 
    
    #check humidity every 20 s
#     if utime.ticks_diff(utime.ticks_ms(), last_dht_check)>= 20000:
#         temp, hum = read_dht11()
#         print("Temperature is:",temp, " Humidity is: ",hum)
#         last_dht_check = utime.ticks_ms()
    
    #check distance every 0.5 s
    if utime.ticks_diff(utime.ticks_ms(), last_dist_check) >= DIST_CHECK_INTERVAL:
        dist = get_distance()
        print("Distance is : ", dist, "cm")
        last_dist_check = utime.ticks_ms()
    
        if 0 < dist < ALERT_THRESHOLD:
            below_alert_duration += DIST_CHECK_INTERVAL
        else:
            below_alert_duration = 0
            
        if below_alert_duration >= DIST_DURATION:
            if buzzer_enabled:
                print("Too close!")
                beep(3)    
                
            else:
                print("Less than 10 cm but Buzzer disabled")
            below_alert_duration = 0
        
    if utime.ticks_diff(utime.ticks_ms(), last_dht_check)>= 2000:    #change to 20000 = 20s when submit, now is 2000 is quick for test uart
        temp, hum = read_dht11()
        light = read_light()
        distance = get_distance()
         
        alert_type = None
         
        if light< LIGHT_THRESHOLD:
            alert_type = "light"
        elif 0 < distance < ALERT_THRESHOLD:
            alert_type = "too_close"
        
        send_uart_data(temp, hum, light, distance, alert_type)
        last_dht_check = utime.ticks_ms()
         
        
utime.sleep(2)
    


