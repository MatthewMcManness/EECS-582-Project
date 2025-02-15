import time
from waveshare_epd import epd2in1
from PIL import Image, ImageDraw, ImageFont

# Initialize the e-ink display
epd = epd2in1.EPD()
epd.init()

# Clear the display
epd.Clear()

# Set the count variable
count = 0

# Create a blank image for drawing
width, height = epd.height, epd.width  # Define width and height based on the display
image = Image.new('1', (width, height), 255)  # Create a white image

# Set up drawing context
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Loop to increment count and update display
while True:
    # Clear the image
    draw.rectangle((0, 0, width, height), fill=255)

    # Draw the current count
    draw.text((10, 10), f"Count: {count}", font=font, fill=0)

    # Display the image
    epd.display(epd.getbuffer(image))

    # Wait for 1 second, then increment count
    time.sleep(1)
    count += 1
