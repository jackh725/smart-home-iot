import utime
import ujson
from buzzer import beep
from button import is_pressed
from ultrasonic import get_distance
from light_sensor import read_light
from dht11 import read_dht11

LIGHT_THRESHOLD = 20000
ALERT_THRESHOLD = 10  #cm if <10cm beep 3 times
DIST_CHECK_INTERVAL =  5 #s
DIST_DURATION = 5   #s

last_light_check = utime.ticks_ms()
last_dht_check = utime.ticks_ms()

below_alert_duration = 0
close_duration = 0

buzzer_enabled = True
prev_btn_state = 0

while True:
    #btn test is ok, now turn on and off
    
    current_state = is_pressed()
    if current_state == 1 and prev_btn_state ==0:
        
        buzzer_enabled = not buzzer_enabled
        print("Button State is:", "Enable" if buzzer_enabled else "Disabled")
        beep(1)
        #uart later
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
    if utime.ticks_diff(utime.ticks_ms(), last_dht_check)>= 20000:
        temp, hum = read_dht11()
        print("Temperature is:",temp, " Humidity is: ",hum)
        last_dht_check = utime.ticks_ms()
    
    #check distance every 0.5 s
    dist = get_distance()
    print("Distance is : ", dist, "cm")
    
    if 0 < dist < ALERT_THRESHOLD:
        
        below_alert_duration += DIST_CHECK_INTERVAL
    else:
        below_alert_duration = 0
        
    if below_alert_duration >= DIST_DURATION:
        if buzzer_enabled:
            print("Proximity Alert!")
            beep(3)    
            
        else:
            print("Less than 10 cm but Buzzer disabled")
        below_alert_duration = 0
        
utime.sleep(DIST_CHECK_INTERVAL)
    


