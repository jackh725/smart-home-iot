from machine import ADC, Pin

light_sensor = ADC(Pin(26))

#LIGHT_THRESHOLD= 20000

def read_light():
    return light_sensor.read_u16()
