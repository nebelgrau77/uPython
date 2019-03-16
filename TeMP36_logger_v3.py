#temperature logger based on TMP36 sensor and ESP8266

from machine import ADC
from machine import Pin
import time

adc = ADC(0) #set up AD converter to pin A0
led = Pin(2, Pin.OUT) #set up built-in LED (pin 2); initial state: on
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
    
    if time.time() >= prev_time + 10: #if 10 seconds have passed since previous time: 

        prev_time = time.time() #update the counter

        led.value(not led.value()) #turn the LED on
        
        celsius_temp = getTemp() #get the current temperature

        if celsius_temp > maxTemp: #if the current temperature is higher than maxTemp
            maxTemp = celsius_temp #update maxTemp
            maxTime = time_decoder(time.time()) #register at what time the new maximum occured
        elif celsius_temp < minTemp: #as above for the minimum
            minTemp = celsius_temp  
            minTime = time_decoder(time.time())
    
        print('\ncurrent temperature: {:.2f}°C\nmaximum temperature: {:.2f}°C @ {:02d}:{:02d}:{:02d}\nminimum temperature: {:.2f}°C @ {:02d}:{:02d}:{:02d}'.format
        (celsius_temp, maxTemp, maxTime[0], maxTime[1], maxTime[2], minTemp, minTime[0], minTime[1], minTime[2])) 
        #print the current temperature and the maximum and minimum with their time stamps
    
        led.value(not led.value()) #turn the LED off