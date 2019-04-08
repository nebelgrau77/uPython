# This is your main script.

import machine, ssd1306, uos
from struct import unpack
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)

oled.fill(1)
oled.show()


while True:

    pixels = uos.urandom(8)
    for n in range(0,8,2):
        oled.pixel(int(pixels[n]/2), int(pixels[n+1]/4),0)
        
    oled.show()
