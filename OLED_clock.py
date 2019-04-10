#analog clock with ESP8266 and OLED

import machine, ssd1306, math, time

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)

center = (63,31)
face_radius = 30

long_hand = 25
short_hand = 15

def coordinates(n,divider, radius):
    '''calculate coordinates of a point on the circle'''
    
    x = int(center[0] + radius * math.cos(n*2*math.pi/divider))
    y = int(center[1] + radius * math.sin(n*2*math.pi/divider))
    
    return x,y

def time_decoder(timestamp):
    '''extract hours and minutes from a timestamp expressed in seconds since Epoch'''

    full_time = time.localtime(timestamp)
    hours = full_time[3]%12
    minutes = full_time[4]

    return hours, minutes

prev_time = time.time() #get the initial timestamp

print(time_decoder(prev_time))

while True:

    current_time = time.time() #get current time

    hours, minutes = time_decoder(current_time)

    hours = (hours + 9)%12 #adjust for the phase of the point calculating function: noon is at 9
    minutes = (minutes + 45)%60 #adjust for the phase of the point calculating function: 00 is at 45
    
    for dot in range(0,12):
        x,y = coordinates(dot,12,face_radius) #draw twelve dots around the clock face
        oled.pixel(x,y,1)

    lhx, lhy = coordinates(minutes,60,long_hand)
    oled.line(center[0],center[1],lhx,lhy,1)

    shx, shy = coordinates(hours,12,short_hand)
    oled.line(center[0], center[1],shx,shy,1)

    oled.show()

    if time.time() > prev_time + 60: #if 60 seconds have passed since previous time: 

        prev_time = time.time() #update the counter
        oled.fill(0) #clean the display
        oled.show()
        print(time_decoder(prev_time))
