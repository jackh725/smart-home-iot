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
    
    timeout= 10000000  #10s 
    start = 0
    end =0 
    try:
        start_time = utime.ticks_us()
        while sig_pin.value() == 0:
            if utime.ticks_diff(utime.ticks_us(), start_time)> timeout:
                return -1
        start = utime.ticks_us()
        
        while sig_pin.value() == 1:
            if utime.ticks_diff(utime.ticks_us(), start_time)> timeout:
                return -1
        end = utime.ticks_us()
        
        duration = utime.ticks_diff(end, start)
        distance = (duration * 0.0343)/2
    
        return distance
    
    except:
        return -1
