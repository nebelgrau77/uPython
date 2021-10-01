import socket
from machine import Pin
led = Pin(4, Pin.OUT)
allow = True
led.value(0)

def instance():
    host = '192.168.43.201'
    print(host)
    port = 2000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    conn, addr = s.accept()

    print("Waiting For Connection: ")
    print("Got connection from" + str(addr))

    while(allow):
        data = conn.recv(1024).decode()
        if not data:
            break
        print("From Connected User ->" + str(data))
        val = str(data)

        if val == '1':
            led.value(1)
            print("Button is Closed")
        if val == '0':
            led.value(0)
            print("Button is Open")


    conn.close()


if __name__ == '__main__':
    instance()
