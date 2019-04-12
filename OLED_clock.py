#analog clock with ESP8266 and SSD1306 OLED display

import machine, ssd1306, math, time

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4)) #setup the I2C protocol for the display
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c) #set up the display
rtc = machine.RTC() #initiate the RealTimeClock

#setup clock elements

center = (31,31) #center of the clock in pixels
face_radius = 30 
long_hand = 25 #length of the minutes hand
short_hand = 15 #length of the hours hand


def coordinates(angle,radius):
    '''calculate coordinates of a point on the circle given angle and radius'''
    
    x = int(center[0] + radius * math.cos(angle))
    y = int(center[1] + radius * math.sin(angle))
   
    return x,y

def time_decoder(timestamp):
    '''extract hours and minutes from a timestamp expressed in seconds since Epoch'''

    full_time = time.localtime(timestamp) #returns a tuple
    hours = full_time[3]%12 #fourth element is hours in 24hrs format
    minutes = full_time[4] #fifth element is minutes

    return hours, minutes

def calc_angle(n):
    '''convert a point on the circle into angle'''
    angle = n*2*math.pi
    return angle


def draw_clockface():
    '''draw 12 equidistant points around the center'''
    
    for dot in range(0,12):
        angle = calc_angle(dot/12)    
        x,y = coordinates(angle,face_radius)
        oled.pixel(x,y,1)

#set the current time after board reset

year = input('enter year: ')
month = input('enter month: ')
day = input('enter day: ')
dayofweek = input('enter day of week (Monday is 1): ')
hours = input('enter hours: ')
minutes = input('enter minutes: ')

rtc.datetime((int(year), int(month), int(day), int(dayofweek), int(hours), int(minutes),0,0))


def conversion(hours, minutes):

    hours_n = (((hours%12)+9)*5 + ((minutes%60)//12))/60 #takes care of the big hand movement, adjust for the sin/cos phase
    minutes_n = ((minutes%60)+45)/60 #adjust for the sin/cos phase

    return hours_n, minutes_n


def draw_hands_time(hours,minutes,color):

    hours_n, min_n = conversion(hours, minutes)

    hrs_angle = calc_angle(hours_n)
    min_angle = calc_angle(min_n)
    
    lhx, lhy = coordinates(min_angle, long_hand)
    oled.line(center[0],center[1],lhx,lhy,color)

    shx, shy = coordinates(hrs_angle,short_hand)
    oled.line(center[0],center[1],shx,shy,color)

    oled.show()

#main program

draw_clockface()

#oled.text('T:25C', 83,0)   #additional info to be shown on the screen, eg. sensor readings
#oled.text('H:70%', 83,24)
#oled.show()

prev_time = time.time() 
hrs, mins = time_decoder(prev_time) #get the initial time

draw_hands_time(hrs,mins,1) #draw the hands for the first time



while True:
        if time.time() > prev_time + 60: #if 60 seconds have passed
                prev_time = time.time() #update the prev_time variable
                draw_hands_time(hrs,mins,0) #cancel the previously drawn hands
                mins += 1 #increment minutes by 1
                
                if mins%60 == 0: #every 60 minutes
                        hrs += 1 #increment hours by 1
                        
                draw_hands_time(hrs,mins,1) #draw new hands
                
