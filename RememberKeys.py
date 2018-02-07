# MIT License
# 
# Copyright (c) 2018 Alessio Leoncini
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import RPi.GPIO as GPIO
import pygame
import time

# Define possible states
class RoomStates:
    DOOR_CLOSED = 1
    SOMEONE_ENTERING = 2
    SOMEONE_EXITING = 3

# Configure pin numbers
PIN_MAGNETIC = 8
PIN_PIR = 7

try:
    # Load audio file
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/tookthekeys.mp3")

    # Disable GPIO warnings
    GPIO.setwarnings(False)
    # Set pin mode (GPIO.BOARD follows the board numbering, 
    # GPIO.BCM follows the broadcom chipset pin numbering)
    GPIO.setmode(GPIO.BOARD)
    # Magnetic sensor input pin, pulldown
    GPIO.setup(PIN_MAGNETIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    # Read output from PIR motion sensor
    GPIO.setup(PIN_PIR, GPIO.IN)

    # Read pin state and debounce 
    def ReadDebounce(pin, debounceTime):
        value = 1
        valueReading = True
        # Read the pin value, and return it only when it seems stable
        # for debouncetime seconds
        while valueReading:
            value = GPIO.input(pin)
            while True:
                time.sleep(debounceTime / 2)
                if GPIO.input(pin) != value:
                    break
                else:
                    time.sleep(debounceTime / 2)
                    if GPIO.input(pin) != value:
                        break
                    else:
                        valueReading = False
                        break
        return value

    # Play audio file
    def PlayReminder():
        # Play wave file
        pygame.mixer.music.play()
        # Wait for audio file end
        while pygame.mixer.music.get_busy() == True:
            continue

    # Check state of system
    def CheckState():
        door = ReadDebounce(PIN_MAGNETIC, 0.5)
        pir = ReadDebounce(PIN_PIR, 0.5)
        # If magnetic contact is closed and input pin
        # is connected to vcc, door is closed
        if door == 1:
            return RoomStates.DOOR_CLOSED
        # If door is opened but pir is 
        elif pir == 0:
            return RoomStates.SOMEONE_ENTERING
        else:
            return RoomStates.SOMEONE_EXITING
    
    # Wait for door closed
    while CheckState() != RoomStates.DOOR_CLOSED:
        continue
    
    # Main cycle
    while True:
        currentState = CheckState()
        # If someone exiting, play audio and wait for door closed
        if currentState == RoomStates.SOMEONE_EXITING:
            print "Remember your keys!"
            PlayReminder()
            while CheckState() != RoomStates.DOOR_CLOSED:
                continue
        # If someone entering, do nothing and wait for door closed
        elif currentState == RoomStates.SOMEONE_ENTERING:
            while CheckState() != RoomStates.DOOR_CLOSED:
                continue

except:
    print "Goodbye..."

finally:
    GPIO.cleanup()