from machine import Pin

button = Pin(18, Pin.IN,Pin.PULL_DOWN)

# while True:
#     print(button.value())
#     time.sleep(0.2)

def is_pressed():
    return button.value() == 1
