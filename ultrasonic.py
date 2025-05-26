from machine import Pin
import utime

sig_pin = Pin(14, Pin.OUT)

def get_distance():
    sig_pin.init(Pin.OUT)
    sig_pin.value(0)
    utime.sleep_us(2)
    sig_pin.value(1)
    utime.sleep_us(10)
    sig_pin.value(0)
    
    sig_pin.init(Pin.IN)
    
    try:
        while sig_pin.value() == 0:
            start = utime.ticks_us()
        while sig_pin.value() == 1:
            end = utime.ticks_us()
            
    except:
        return -1
    
    duration = utime.ticks_diff(end, start)
    distance = (duration * 0.0343)/2
    
    return distance
