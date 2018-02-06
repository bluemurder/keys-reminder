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
        # If 
        elif pir == 0:
            return RoomStates.SOMEONE_ENTERING
        else:
            return RoomStates.SOMEONE_EXITING
    
    # Wait for door closed
    while CheckState() != RoomStates.DOOR_CLOSED:
        continue
    
    # Main cycle
    while True:
        if CheckState() == RoomStates.SOMEONE_EXITING:
            print "Remember your keys!"
            PlayReminder()
            while CheckState() != RoomStates.DOOR_CLOSED:
                continue

except:
    print "Goodbye..."

finally:
    GPIO.cleanup()