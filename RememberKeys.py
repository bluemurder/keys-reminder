import RPi.GPIO as GPIO
import pygame

# Configure pin numbers
PIN_MAGNETIC = 8
PIN_PIR = 3
PIN_LED = 7

# Load audio file
pygame.mixer.init()
pygame.mixer.music.load("/home/pi/myFile.wav")

# Define callback
def doorIsOpening():
    # Turn on LED
    GPIO.output(PIN_LED, 1)
    # Check if PIR detects anyone close to the door.
    # In this case it is probably anyone leaving home
    if GPIO.input(PIN_PIR) == 1:
        # Play wave file
        pygame.mixer.music.play()
        # Wait for audio file end
        while pygame.mixer.music.get_busy() == True:
            continue
    # Turn off LED
    GPIO.output(PIN_LED, 0)

# Set pin mode (GPIO.BOARD follows the board numbering, 
# GPIO.BCM follows the broadcom chipset pin numbering)
GPIO.setmode(GPIO.BOARD)
# Magnetic sensor input pin, pulldown
GPIO.setup(PIN_MAGNETIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# LED pin, output
GPIO.setup(PIN_LED, GPIO.OUT, initial = GPIO.LOW)
# Read output from PIR motion sensor
GPIO.setup(PIN_PIR, GPIO.IN)

# Add event callback when magnetic sensor detects that door is opening
# It is assumed that when door opens, the magnetic sensor pin
# presents a falling edge
GPIO.add_event_detect(PIN_MAGNETIC, GPIO.FALLING, callback = doorIsOpening, bouncetime = 2000)