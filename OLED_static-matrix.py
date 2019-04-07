# This is your main script.

import machine, ssd1306, uos    #, time
from struct import unpack
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)

while True:
    for x in range(128):
        for y in range(64):
            val = uos.urandom(1)[0]%2
            oled.pixel(x,y,val)
            oled.show() #if put here, it creates a `Matrix` style falling random pixels
    #oled.show() # if put here it refreshes the new noisy screen every time the generation is completed
