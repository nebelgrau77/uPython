#temperature logger based on TMP36 sensor and ESP8266 with OLED SSD1306 display

import machine, ssd1306, time
i2c = machine.I2C(scl = machine.Pin(5), sda = machine.Pin(4)) #SCL: 4th pin marked D15/SCL on Wemos D1 R2 board, SDA: 5th pin (D14/SDA)
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
adc = machine.ADC(0) #TMP36 sensor at pin A0
led = machine.Pin(2, machine.Pin.OUT) #set up built-in LED (pin 2); initial state: on
led.value(not led.value()) #turn the LED off

def getTemp():
    '''convert the voltage read from the TMP36 sensor to temperature in Celsius
    reference voltage 3.3V, sensor offset 500mV, 10bit ADC with values 0..1023
    '''
    temp = (((adc.read()*3.3)/(1023))-0.5)*100 
    return temp

prev_time = time.time() #get the initial timestamp

def time_decoder(timestamp):
    '''translates the timestamp in seconds since Epoch into a 3-element tuple with hours, minutes and seconds'''
    full_time = time.localtime(timestamp)
    return (full_time[3], full_time[4], full_time[5])

maxTemp = getTemp() #initiate maxTemp value
maxTime = time_decoder(time.time()) #initiate maxTime value
minTemp = getTemp() #initiate minTemp value
minTime = time_decoder(time.time()) #initiate minTime value

while True:
    
    if time.time() >= prev_time + 5: #if 30 seconds have passed since previous time: 

        prev_time = time.time() #update the counter

        led.value(not led.value()) #turn the LED on
        
        celsius_temp = getTemp() #get the current temperature

        if celsius_temp > maxTemp: #if the current temperature is higher than maxTemp
            maxTemp = celsius_temp #update maxTemp
            maxTime = time_decoder(time.time()) #register at what time the new maximum occured
        elif celsius_temp < minTemp: #as above for the minimum
            minTemp = celsius_temp  
            minTime = time_decoder(time.time())
    
        currentTime = time_decoder(time.time())

        oled.fill(0) #clear up the display
        

        #create text strings for the displays

        currentTimeText = 'time: {:02d}:{:02d}:{:02d}'.format(currentTime[0], currentTime[1], currentTime[2]) 
        currentTempText = 'T: {:.2f}C'.format(celsius_temp)
        maxTempText = 'max T: {:.2f}C'.format(maxTemp)
        minTempText = 'min T: {:.2f}C'.format(minTemp)


        oled.text(currentTimeText,0,0) #display at column 0, row 0
        oled.text(currentTempText,0,15) #display at column 0, row 15 etc.
        oled.text(maxTempText,0,30)
        oled.text(minTempText,0,45)

       
        oled.show()

        led.value(not led.value()) #turn the LED off




