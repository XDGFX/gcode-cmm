#!/usr/bin/env python3

import json
import serial
import time
import sys
import termios
import tty
import os
import csv


def read_settings():
    with open("settings.json") as settings_json:
        settings = json.load(settings_json)
        return settings


def open_serial():
    print("Connecting to serial...")
    s = serial.Serial(settings["port"], settings["baud"])

    s.write("\r\n\r\n".encode())  # Wake up serial device
    time.sleep(2)   # Wait for initialisation
    s.flushInput()  # Flush startup text
    return s


def send_gcode(l):
    l = l.strip()  # Strip all EOL characters for streaming

    for line in l.splitlines():
        if (line.isspace() == False and len(line) > 0):
            line = line + "\n"
            s.write(line.encode())  # Send g-code block
            while (s.inWaiting() > 0):
                response = s.readline().decode().strip()


def gotopoint():
    # Lift to starting Z position
    send_gcode(f"G0Z{CMM.start[2]}")

    point = CMM.point_list[CMM.point]

    # Goto X, Y position
    send_gcode(f"G0X{point[0]}Y{point[1]}")

    CMM.pos = [point[0], point[1], CMM.start[2]]


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


class CMM:
    point = 0  # Current point out of total
    point_list = []

    # CMM start position [x, y, z]
    start = [0, 0, 0]

    # Current head position [x, y, z]
    pos = [0, 0, 0]

    # Saved datapoints
    datapoints = []


startup_gcode = """
M107 P1 ; Turn off part fan
G28 ; Home all axes
G1 Z50 F5000 ; Move Z Axis up to allow attachment of CMM
"""

settings = read_settings()
s = open_serial()

# Send startup GCODE and update variables correctly
print("Sending startup GCODE")
send_gcode(startup_gcode)
CMM.pos[2] = 50

# Perform initial position calibration
print(f"\033[1mINITIAL CALIBRATION\033[0m")
print(f"\033[95m\033[1mX\033[0m: Exit\
    \033[95m\033[1mE\033[0m: Z Up\
    \033[95m\033[1mQ\033[0m: Z Down\
    \033[95m\033[1mW\033[0m: Y Up\
    \033[95m\033[1mS\033[0m: Y Down\033[0m\
    \033[95m\033[1mA\033[0m: X Up\033[0m\
    \033[95m\033[1mD\033[0m: X Down\033[0m\
    \033[95m\033[1mY\033[0m: Accept Start Position\033[0m")

while True:
    char = getch()

    if (char == "x"):
        exit(0)

    if (char == "e"):
        # Increment Z by 1mm and send new position
        CMM.pos[2] += 1
        send_gcode("G0Z" + str(CMM.pos[2]))

    if (char == "q"):
        # Decrement Z by 1mm and send new position
        CMM.pos[2] -= 1
        send_gcode("G0Z" + str(CMM.pos[2]))

    elif (char == "w"):
        # Increment Y by 5mm and send new position
        CMM.pos[1] += 5
        send_gcode("G0Y" + str(CMM.pos[1]))

    elif (char == "s"):
        # Decrement Y by 5mm and send new position
        CMM.pos[1] -= 5
        send_gcode("G0Y" + str(CMM.pos[1]))

    elif (char == "a"):
        # Decrement X by 5mm and send new position
        CMM.pos[0] -= 5
        send_gcode("G0X" + str(CMM.pos[0]))

    elif (char == "d"):
        # Increment X by 5mm and send new position
        CMM.pos[0] += 5
        send_gcode("G0X" + str(CMM.pos[0]))

    elif (char == "y"):
        print("Accepted position")
        CMM.start = CMM.pos
        break

# Create all remaining measurement points
for x in range(settings["points_x"]):
    pos_x = CMM.start[0] + x / (settings["points_x"] - 1) * settings["dist_x"]

    for y in range(settings["points_y"]):
        pos_y = CMM.start[1] + y / \
            (settings["points_y"] - 1) * settings["dist_y"]

        CMM.point_list.append([pos_x, pos_y])

# Create datapoints list with correct length
print("Initialising datapoints list...")
CMM.datapoints = [0] * len(CMM.point_list)

# Go to fist point
gotopoint()

print(f"\033[95m\033[1mX\033[0m: Quit\033[0m\
    \033[95m\033[1mW/I\033[0m: Z Up\033[0m\
    \033[95m\033[1mS/K\033[0m: Z Down\033[0m\
    \033[95m\033[1mD\033[0m: Next Grid Point\033[0m\
    \033[95m\033[1mA\033[0m: Previous Grid Point\033[0m\
    \033[95m\033[1mE\033[0m: Save & Next Grid Point\033[0m")

while True:
    char = getch()

    if (char == "x"):
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
        # Increment Z by 1mm and send new position
        CMM.pos[2] += 1
        send_gcode("G0Z" + str(CMM.pos[2]))

    elif (char == "s"):
        # Decrement Z by 1mm and send new position
        CMM.pos[2] -= 1
        send_gcode("G0Z" + str(CMM.pos[2]))

    if (char == "i"):
        # Increment Z by 1mm and send new position
        CMM.pos[2] += 0.1
        send_gcode("G0Z" + str(CMM.pos[2]))

    elif (char == "k"):
        # Decrement Z by 1mm and send new position
        CMM.pos[2] -= 0.1
        send_gcode("G0Z" + str(CMM.pos[2]))

    elif (char == "a"):
        if CMM.point > 0:
            CMM.point -= 1
            gotopoint()

    elif (char == "d"):
        if CMM.point < len(CMM.point_list) - 1:
            CMM.point += 1
            gotopoint()

    elif (char == "e"):
        CMM.datapoints[CMM.point] = CMM.pos

        if CMM.point < len(CMM.point_list) - 1:
            CMM.point += 1
            gotopoint()
        else:
            print("All points complete! Saving to file...")
            print(CMM.datapoints)

            with open(settings["output_file"], "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(CMM.datapoints)

            # Go back to home
            send_gcode(f"G0Z{CMM.start[2]}")
            send_gcode(f"G0X0Y0")
            send_gcode(f"G0Z0")
            exit(0)
