import robotbit_library as r
from microbit import *
from time import sleep_us
from machine import time_pulse_us
import radio


S1 = 0x1  # used for standard servo
S2 = 0x2  # used for continuous servo in this example
S3 = 0x3
S4 = 0x4
S5 = 0x5
S6 = 0x6
S7 = 0x7
S8 = 0x8

TIME_OUT = 100000  # Increase time out to see farther, but
# this will reduce the sample rate
ECHO = pin1  # ping sensor uses a single pin for ECHO and Trigger
TRIGGER = pin1


def distance(tp, ep):
    # tp is the trigger pin and ep is the echo pin
    ep.read_digital()  # clear echo
    tp.write_digital(1)  # Send a 10 microSec pulse
    sleep_us(10)  # wait 10 microSec
    tp.write_digital(0)  # Send pulse low
    ep.read_digital()  # clear echo signal - This is needed for a
    # pingSensor
    ts = time_pulse_us(ep, 1, TIME_OUT)  # Wait for echo or time out
    if ts > 0:
        ts = ts * 17 // 100  # if system did not timeout, then send
        # back a scaled value
    return ts  # Return timeout error as a negative number (-1)


def main():
    r.setup()
    counter = 0
    r.servo(S8, 0) #Set up initial servo position
    display.show("U")  # provide feedback that Ping sensor is running
    rush = False
    save = False
    # stop = False
    while True:
        a = button_a.is_pressed()
        b = button_b.is_pressed()
        # print(a)
        print(a)
        if a:
            if (rush == False):
                rush = True
                if save == True:
                    save = False
            else:
                rush = False
        if b:
            if (save == False):
                save = True
                if (rush == True):
                    rush = False
            else:
                save = False
        print(rush)
        # regular mode
        if rush == False and save == False:
            # press button to make sign swivel
            a = pin2.is_touched()
            if counter <= 0:
                if a:
                    r.servo(S8, 107)
                    for i in range(10):
                        if i < 5:
                            display.show(Image.ARROW_E)
                        else:
                            display.show(10 - i)
                        sleep(1000)
                    display.show(0)
                    sleep(1000)
                    r.servo(S8, 0)
                    display.show(Image.NO)
                    sleep(5000)

            # ultrasonic sensor
            dist = distance(TRIGGER, ECHO)  # set up to read as a ping)))
            if dist > 100 and counter <= 0:
                display.show(Image.YES)
                counter = 0
                sleep(500)
            elif dist > 100 and counter > 0:
                display.show(Image.NO)
                counter -= 1000
                sleep(500)
            if dist < 100:
                display.show(Image.NO)
                counter = 10000
                sleep(500)
            # sensor same pin
            print(dist, counter)  # use serial terminal to get information
            sleep(500)  # set for a slow update rate

        # rush hour mode
        elif rush == True:
            rush = False
            print(rush)
            for i in range(2):
                r.servo(S8, 107)
                for i in range(10):
                    if i < 5:
                        display.show(Image.ARROW_E)
                    else:
                        display.show(10 - i)
                        sleep(1000)
                display.show(0)
                sleep(1000)
                r.servo(S8, 0)
                display.show(Image.NO)
                for i in range(5):
                    sleep(1000)

        # power saving mode
        elif save == True:
            display.clear()
            dist = distance(TRIGGER, ECHO)  # set up to read as a ping)))
            if dist > 100 and counter <= 0:
                # display.show(Image.YES)
                counter = 0
                sleep(500)
            elif dist > 100 and counter > 0:
                display.set_pixel(1, 1, 3)
                display.set_pixel(1, 3, 3)
                display.set_pixel(2, 2, 3)
                display.set_pixel(3, 1, 3)
                display.set_pixel(3, 3, 3)
                counter -= 1000
                sleep(500)
            if dist < 100:
                display.set_pixel(1, 1, 3)
                display.set_pixel(1, 3, 3)
                display.set_pixel(2, 2, 3)
                display.set_pixel(3, 1, 3)
                display.set_pixel(3, 3, 3)
                counter = 10000
                sleep(500)
            # sensor same pin
            print(dist, counter)  # use serial terminal to get information
            sleep(500)


if __name__ == "__main__":
    main()
