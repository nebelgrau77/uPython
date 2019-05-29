# reads RFID tags and prints them to the console as a tuple of integers
# needs mfrc522 from https://github.com/wendlers/micropython-mfrc522

import mfrc522

reader = mfrc522.MFRC522(14, 13, 12, 0, 2) 
# initiate RC522 reader with the following pins: 
# SCK pin 14 (D13), MOSI pin 13 (D11), MISO pin 12 (D12), RST pin 0 (D8), SDA/CS pin 2 (D9)

while True:
	
    (stat, tag_type) = reader.request(reader.REQIDL) #read the RFID tag

    if stat == reader.OK: #check if OK
        (stat, raw_uid) = reader.anticoll() #get the unique ID
            
        card_id = (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3], raw_uid[4])

        print(card_id)
    
    
