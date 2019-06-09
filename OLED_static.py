# static noise

import machine, ssd1306, uos, framebuf

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)


while True:

    noise = bytearray(uos.urandom(1024)) # generate 1024 random bytes (128 pixels = 16 bytes, 16 x 64 lines = 1024 bytes)
    fbuf = framebuf.FrameBuffer(noise, 128, 64, framebuf.MONO_VLSB) #create a framebuffer with the random pixels
    oled.blit(fbuf,0,0) #blit the buffer at 0,0 coordinates
    oled.show()


