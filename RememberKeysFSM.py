import RPi.GPIO as GPIO
import pygame
import time

# Define possible states
class RoomState:
    DOOR_CLOSED = 1
    SOMEONE_ENTERING = 2
    SOMEONE_EXITING = 3

# Configure pin numbers
PIN_MAGNETIC = 8
PIN_PIR = 5 # TODO Check this
PIN_LED = 7

# Load audio file
pygame.mixer.init()
pygame.mixer.music.load("/home/pi/myFile.wav")

# Set pin mode (GPIO.BOARD follows the board numbering, 
# GPIO.BCM follows the broadcom chipset pin numbering)
GPIO.setmode(GPIO.BOARD)
# Magnetic sensor input pin, pulldown
GPIO.setup(PIN_MAGNETIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# LED pin, output
GPIO.setup(PIN_LED, GPIO.OUT, initial = GPIO.LOW)
# Read output from PIR motion sensor
GPIO.setup(PIN_PIR, GPIO.IN)

# Read pin state and debounce 
def ReadDebounce(pin, debounceTime):
    value = 1
    valueReading = True
    # Read the pin value, and return it only when it is stable
    # for debouncetime seconds
    while valueReading:
        value = GPIO.input(pin)
        while True:
            time.sleep(debounceTime / 2)
            if GPIO.input(pin) == value:
                time.sleep(debounceTime / 2)
                    if GPIO.input(pin) == value:
                        valueReading = False
                        break
    return value

# 
def PlayReminder:
    # Turn on LED
    GPIO.output(PIN_LED, 1)
    # Play wave file
    pygame.mixer.music.play()
    # Wait for audio file end
    while pygame.mixer.music.get_busy() == True:
        continue
    # Turn off LED
    GPIO.output(PIN_LED, 0)

# 
def CheckState:
    door = ReadDebounce(PIN_MAGNETIC, 0.5)
    pir = ReadDebounce(PIN_PIR, 0.5)
    if door == 0:
        return RoomState.DOOR_CLOSED
    elif pir == 0:
        return RoomState.SOMEONE_ENTERING
    else
        return RoomState.SOMEONE_EXITING

# Wait for door closed
while CheckState() not RoomState.DOOR_CLOSED:
    continue

# Main cycle
while True:
    if CheckState() == RoomState.SOMEONE_EXITING:
        PlayReminder()
        while CheckState() not RoomState.DOOR_CLOSED:
            continue
