import os
import time

import pyautogui
import wiringpi

EOA_PIN = 13  # PC7   Encoder Out A
EOB_PIN = 16  # PC10  Encoder Out B
ES_PIN = 6  # PC11  Encoder Switch

POLLING_PERIOD = 2  # in milliseconds
SHUTDOWN_DELAY = 5  # in seconds

X_MOUSE_OFFSET = 20  # in pixels
Y_MOUSE_OFFSET = 20  # in pixels

pyautogui.FAILSAFE = False

wiringpi.wiringPiSetup()
wiringpi.pinMode(EOA_PIN, wiringpi.GPIO.INPUT)
wiringpi.pinMode(EOB_PIN, wiringpi.GPIO.INPUT)
wiringpi.pinMode(ES_PIN, wiringpi.GPIO.INPUT)

get_left = lambda: wiringpi.digitalRead(EOA_PIN)
get_right = lambda: wiringpi.digitalRead(EOB_PIN)
get_switch = lambda: wiringpi.digitalRead(ES_PIN)

left = right = switch = wiringpi.GPIO.HIGH


def read_state(delay=POLLING_PERIOD):
    global left, right, switch
    wiringpi.delay(delay)
    left = get_left()
    right = get_right()
    switch = get_switch()


def wait_release_all():
    while not (left == 1 and right == 1 and switch == 1):
        read_state()


def wait_release_left_right():
    while not (left == 1 and right == 1):
        read_state()


alt_flag = False

while True:
    read_state()

    if left != right and switch:
        if left == 0:
            pyautogui.moveRel(-X_MOUSE_OFFSET, 0)
        elif right == 0:
            pyautogui.moveRel(X_MOUSE_OFFSET, 0)
        wait_release_all()

    elif not switch:
        start = time.time()

        while True:
            read_state()

            if left != right:
                alt_flag = True
                if left == 0:
                    pyautogui.moveRel(0, -Y_MOUSE_OFFSET)
                elif right == 0:
                    pyautogui.moveRel(0, Y_MOUSE_OFFSET)
                wait_release_left_right()

            elif switch:
                if not alt_flag:
                    pyautogui.click(button='left')
                alt_flag = False
                wait_release_all()
                break

            elif all(
                (
                    not alt_flag,
                    not switch,
                    time.time() - start > SHUTDOWN_DELAY,
                )
            ):
                os.system('shutdown now')
