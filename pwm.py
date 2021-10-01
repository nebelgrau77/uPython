from machine import PWM
# frequency ranges upto 1Hz and Duty scycle of 512
led = PWM(4, freq=1000, duty=512)
# Connect your LED to D2 or GPIO4 of NodeMCU
# First it starts from 0 duty cycle and ends to 510
try:
    for i in range(0, 511, 5):
        led.duty(i)
        print(i)
    # then it recides from 510 to 0 and then deinitlises the process
    for i in range(510, -5, -5):
        led.duty(i)
        print(i)

    led.deinit()  # Deinitialises the process
except KeyboardInterrupt:
    print("User ended the Program, bye...!!!!")
