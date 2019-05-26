# reads RFID tags, displays the associated card suit and the time of tag scan (still to be improved)
# needs ds1307 module from https://github.com/mcauser/micropython-tinyrtc-i2c
# needs mfrc522 from https://github.com/wendlers/micropython-mfrc522

import machine, ds1307, ssd1306, time, mfrc522

i2c = machine.I2C(scl = machine.Pin(5), sda = machine.Pin(4)) #set up the I2C
oled = ssd1306.SSD1306_I2C(128,32,i2c,0x3c) #set up the display
ds = ds1307.DS1307(i2c,0x68) #set up the TinyRTC

reader = mfrc522.MFRC522(14, 13, 12, 0, 2) 
# initiate RC522 reader with the following pins: 
# SCK pin 14 (D13), MOSI pin 13 (D11), MISO pin 12 (D12), RST pin 0 (D8), SDA/CS pin 2 (D9)

deck = {(136,4,110,155,121):'DIAMONDS', (136,4,218,48,102):'HEARTS', (136,4,124,155,107):'SPADES', (136,4,123,155,108):'CLUBS'}
#tuples are uids of the discarded bus tickets with RFID tags, with card suits marked on them :)

def display(id, timestamp):
    '''clears the display, then displays the id and timestamp in two lines''' 
    # needs to stay on for a defined amount of time, then disappear

    digits = "{:02d}:{:02d}:{:02d}".format(timestamp[4], timestamp[5], timestamp[6])
    oled.fill(0)
    oled.text(id, 0, 0)
    oled.text(digits, 0, 16)
    oled.show()


while True:
	
    (stat, tag_type) = reader.request(reader.REQIDL) #read the RFID tag

    if stat == reader.OK: #check if OK
        (stat, raw_uid) = reader.anticoll() #get the unique ID
            
        card_id = deck[(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3], raw_uid[4])] #get the card name from dictionary
                       
    else:
        card_id = 'unknown' #if tag not OK - need to fix this, currently stays as 'unknown' when no cards are being read

    scantime = ds.datetime() #get the current time from RTC
    display(card_id, scantime) #call the display function