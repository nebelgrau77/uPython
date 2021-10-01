import socket
from machine import Pin
from time import sleep
btn = Pin(4, Pin.IN)

def clientside():
    host = '192.168.43.201'
    port = 2000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Connection Done!!")
    allow = True

    try:
        while allow:
            btn_state =str(btn.value())
            sleep(0.02)
            print("Button Status ->", btn_state)
            if btn_state =='1':
                data = btn_state
                s.send(data.encode())
                sleep(3)

                print("message sent to server: ", btn_state)
            elif btn_state == '0':
                data = btn_state
                s.send(data.encode())
                print("message sent to server: ", btn_state)
                sleep(3)
        s.close()
        sleep(3)

    except OSError:
        print("ReAttempting...")
        clientside()


if __name__ == '__main__':
    clientside()





