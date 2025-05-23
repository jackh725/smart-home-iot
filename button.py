from machine import Pin

button = Pin(18, Pin.IN, Pin.PULL_DOWN)

def is_pressed():
    return button.value() == 1
