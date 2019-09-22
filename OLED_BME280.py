# static noise

import machine, ssd1306, uos, framebuf, time, bme280_float

i2c = machine.I2C(scl=machine.Pin(21), sda=machine.Pin(22))
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
bme = bme280_float.BME280(i2c = i2c)

while True:

    time.sleep(5)

    vals = bme.values

    oled.fill(0)

    oled.text('T: ' + vals[0], 1, 1, 1)
    oled.text('H: ' + vals[2], 1, 17, 1)
    oled.text('P: ' + vals[1], 1, 33, 1)

    oled.show()
