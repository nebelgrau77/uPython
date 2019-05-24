# This is your main script.

import machine, ds1307, ssd1306, time

i2c = machine.I2C(scl = machine.Pin(5), sda = machine.Pin(4)) #set up the I2C
oled = ssd1306.SSD1306_I2C(128,32,i2c,0x3c) #set up the display
ds = ds1307.DS1307(i2c,0x68) #set up the TinyRTC

while True:    
    now = ds.datetime() #get time from the TinyRTC
    now_digits = "{:02d}:{:02d}:{:02d}".format(now[4], now[5], now[6]) #get hours, minutes and seconds with leading zeros
    oled.fill(0) #clear the display
    oled.text(now_digits,0,0) #print the current time
    oled.show()