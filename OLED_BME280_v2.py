# BME280 with OLED display

from machine import Pin, I2C
import ssd1306, time, bme280_float
from tinypico import set_dotstar_power

set_dotstar_power(False)
i2c = I2C(scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128,32,i2c,0x3c) # small display
bme = bme280_float.BME280(i2c = i2c)

oled.contrast(0) #set contrast to low

def display_weather():
    temp, pres, hum = bme.values

    oled.fill(0)
    oled.text('T: ' + temp, 1, 1, 1)
    oled.text('H: ' + hum, 1, 17, 1)
    #oled.text('P: ' + pres, 1, 33, 1)

    oled.show()

start_time = time.time()
display_weather()

while True:

    if time.time() >= start_time + 60:
        display_weather()
        start_time = time.time()
