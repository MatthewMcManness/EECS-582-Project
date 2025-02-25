"""
Program Name: Increment Count
Description: updates the e-ink display to reflect change in ballot count.

Programmer(s): Ashley Aldave, Manvir Kaur
Creation Date: 02/15/2025
Revisions: 
    - 02/15/2025 Initial Version (Ashley and Manvir)
    - 02/16/2025 Adding Prologue Comments
    - 02/24/2025 Fixing code (Ashley and Manvir)

Preconditions: 
    - Components (button, light curtain, e-ink display) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be updated when a ballot enters the drop box
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
Faults:
    - None known
"""


# GPIO pin for the sensor
SENSOR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Initialize the e-ink display
epd = epd2in13_V2.EPD()
epd.init()
epd.Clear(0xFF)

# Counter variable
count = 0

def update_display(count):
    # Create image for the display
    image = Image.new('1', (epd.width, epd.height), 255)  # 255: white
    draw = ImageDraw.Draw(image)
    
    # Draw the text on the display
    draw.text((10, 30), f"Envelope Count: {count}", &Font12, fill=0)
    
    # Update the display with the new image
    epd.display(epd.getbuffer(image))
    epd.sleep()

def envelope_detected(channel):
    global count
    count += 1
    update_display(count)

# Event to detect when the sensor detects an envelope
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=envelope_detected, bouncetime=300)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    epd.sleep()

