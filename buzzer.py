from machine import Pin
import time

buzzer = Pin(16,Pin.OUT)

def beep(times =1, duration = 0.2, pause = 0.2):
    for _ in range(times):
        buzzer.value(1)
        time.sleep(duration)
        buzzer.value(0)
        time.sleep(pause)