# BME280 with OLED display

from machine import Pin, I2C, RTC
import ssd1306, time, bme280_float
from tinypico import set_dotstar_power

set_dotstar_power(False)
rtc = RTC()
i2c = I2C(scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128,32,i2c,0x3c) # small display
bme = bme280_float.BME280(i2c = i2c)

oled.contrast(0) #set contrast to low

def display_temperature():
    temp, pres, hum = bme.values
    oled.fill(0)
    oled.text('T: ' + temp, 0, 0, 1)
    oled.show()

def display_humidity():
    temp, pres, hum = bme.values
    oled.fill(0)
    oled.text('H: ' + hum, 0, 0, 1)
    oled.show()

def display_pressure():
    temp, pres, hum = bme.values
    oled.fill(0)
    oled.text('P: ' + pres, 0, 0, 1)
    oled.show()
    
def display_time():
    year, month, day, weekday, hours, minutes, seconds, ns = rtc.datetime()
    oled.fill(0)
    oled.text('{:02d}:{:02d}'.format(hours, minutes),0,0,1)
    oled.show()

def display_date():
    year, month, day, weekday, hours, minutes, seconds, ns = rtc.datetime()
    oled.fill(0)
    oled.text('{:04d}-{:02d}-{:02d}'.format(year, month, day),0,0,1)
    oled.show()
    

delay = 2
start_time = time.time()
display_time()

while True:

    time.sleep(delay)
    display_temperature()
    time.sleep(delay)
    display_humidity()
    time.sleep(delay)
    display_pressure()
    time.sleep(delay)
    display_date()
    time.sleep(delay)
    display_time()    
