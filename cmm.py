#!/usr/bin/env python3

import json
import serial
import time
import sys
import termios
import tty
import os


def read_settings():
    with open("settings.json") as settings_json:
        settings = json.load(settings_json)
        return settings


def open_serial():
    print("Connecting to serial...")
    s = serial.Serial(settings["port"], settings["baud"])

    s.write("\r\n\r\n")  # Wake up serial device
    time.sleep(2)   # Wait for initialisation
    s.flushInput()  # Flush startup text
    return s


def send_gcode(l):
    l = l.strip()  # Strip all EOL characters for streaming

    for line in l.splitlines():
        if (line.isspace() == False and len(line) > 0):
            s.write(line + '\n')  # Send g-code block


def getch():
    # Get keyboard input and return value
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


startup_gcode = """
G28 ; Home all axes
G1 Z50 X100 F3000 ; Move Z Axis up to allow attachment of CMM
"""

help_text = f"\033[95m\033[1mQ\033[0m: Quit\033[0m\
    \033[95m\033[1mW\033[0m: Z Up\033[0m\
    \033[95m\033[1mS\033[0m: Z Down\033[0m\
    \033[95m\033[1mD\033[0m: Next Grid Point\033[0m\
    \033[95m\033[1mA\033[0m: Previous Grid Point\033[0m\
    \033[95m\033[1mE\033[0m: Save Position\033[0m"


settings = read_settings()
# s = open_serial()


print(help_text)

# send startup gcode
# calibrate zero position
# calculate number of grid points using distance and number of points
# move to pos 1
# allow user to move down until touching
# save current position to text file
# move up, and to second position


while True:
    char = getch()

    if (char == "q"):
        print("Are you sure you want to quit? [y/n]: ", end="")

        while True:
            char = getch()
            if (char.lower() == "y"):
                exit(0)
            elif (char.lower() == "n"):
                print("Not exiting...")
                break
            else:
                print("Please input y or n: ", end="")

    if (char == "w"):
        print("left Pressed", end="\r")

    elif (char == "s"):
        print("Right pressed")

    elif (char == "a"):
        print("Up pressed")

    elif (char == "d"):
        print("Down pressed")

    elif (char == "e"):
        print("Number 1 pressed")
