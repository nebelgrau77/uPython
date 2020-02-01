
from machine import Pin, I2C, SPI
import time
import tcs34725
import st7735 #adafruit Micropython st7735 driver
from rgb import color565 #rgb.py y adafruit

'''set up the buses'''

i2c = I2C(scl = Pin(21), sda = Pin(22))

spi = SPI(2, baudrate = 20000000, polarity = 0, phase = 0, bits = 8, firstbit = 0, sck = Pin(18), mosi = Pin(23), miso = Pin(19)) 
# gets all screwed up with higher baudrate

'''set up the display'''

display = st7735.ST7735R(spi, dc = Pin(15), cs = Pin(5), rst = Pin(27))

'''set up the sensor'''

sensor = tcs34725.TCS34725(i2c)
sensor.active(True)
sensor.integration_time(100)
sensor.gain(1)

'''set up the sensor illuminating LED'''

led = Pin(33, Pin.OUT)
led.on()

rvals = [0,0,0,0,0]
gvals = [0,0,0,0,0]
bvals = [0,0,0,0,0]

while True:
    r,g,b,_ = sensor.read(True)
    
    rvals = rvals[1:]
    rvals.append(r)
    gvals = gvals[1:]
    gvals.append(g)
    bvals = bvals[1:]
    bvals.append(b)

          

    print('r: {}, g: {}, b: {}'.format(rvals, gvals, bvals))
    
    disp_r, disp_g, disp_b = (int(sum(rvals)/5), int(sum(gvals)/5), int(sum(bvals)/5))

    display.fill(color565(disp_b, disp_g, disp_r)) #BGR color space

    time.sleep_ms(100)
