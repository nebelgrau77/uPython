#temperature logger based on TMP36 sensor and ESP8266

from machine import ADC
from machine import Pin
import time
adc = ADC(0) #set up AD converter to pin A0
led = Pin(2, Pin.OUT) #set up built-in LED (pin 2); initial state: on
led.value(not led.value()) #turn the LED off

def getTemp():
    '''convert the voltage read from the TMP36 sensor to temperature in Celsius
    reference voltage 3.3V, sensor offset 500mV, 10bit ADC therefore 1024 values in total
    '''
    temp = (((adc.read()*3.3)/(1023))-0.5)*100 
    return temp

timestamp = time.localtime() #get the initial time

maxTemp = getTemp() #initiate maxTemp value
maxTime = timestamp #initiate maxTime value
minTemp = getTemp() #initiate minTemp value
minTime = timestamp #initiate minTime value

while True:
    led.value(not led.value()) #turn the LED on
        
    celsius_temp = getTemp() #get the current temperature

    if celsius_temp > maxTemp: #if the current temperature is higher than maxTemp
        maxTemp = celsius_temp #update maxTemp
        maxTime = time.localtime() #register at what time the new maximum occured
    elif celsius_temp < minTemp: #as above for the minimum
        minTemp = celsius_temp  
        minTime = time.localtime()
    

    print('\ncurrent temperature: {:.2f}°C\nmaximum temperature: {:.2f}°C @ {:02d}:{:02d}:{:02d}\nminimum temperature: {:.2f}°C @ {:02d}:{:02d}:{:02d}'.format
        (celsius_temp, maxTemp, maxTime[3], maxTime[4], maxTime[5], minTemp, minTime[3], minTime[4], minTime[5])) 
        #print the current temperature and the maximum and minimum with their time stamps

    led.value(not led.value()) #turn the LED off
   

    time.sleep(10) #wait 10 seconds