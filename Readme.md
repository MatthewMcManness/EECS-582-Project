# User Guide for the "Smart Drop-Box Frame"

### System Overview:
The "Smart Drop-Box Frame" is a system designed to work with a variety ballot drop box designs.  It consists of a collection of hardware attached to a frame that can be dropped into a pre-existing ballot drop box.  This means that if a county would like to upgrade their existing ballot drop boxes into smart drop boxes all they need to do is design the frame structure to fit inside their boxes, attach the hardware, and drop the frame inside to create a Smart Ballot Drop box.

---

### Component Guide:

#### Frame:

The frame should be custom designed to fit the drop box you are enhancing. We are working with the Douglas County Clerk to modify their main (larger) drop boxes and as such we built a frame with the following specifications:
- Made out of dimensional 2x2 pine lumber
- pieces connected through half-lap joints and threaded inserts (with hex bolts)
- hardware attached to the frame using:
    -  threaded inserts (either directly to the frame or to plywood connected to the frame)
    -  zip ties
    or 
    -  directly with clamps

The following is a list of the cuts made to the dimensional lumber (not including the joints):

**Components List**
| Piece ID | # Needed | Dimensions (in inches) | Description |
| -------- | -------- | -------- | -------|
| A.1    | 2     | 39 x 2 x 2     | Back Vertical columns|
| A.2    | 2     | 43 x 2 x 2     | Front Vertical columns |
| B    | 4     | 18 3/4 x 2 x 2     | Front/Back beams |
| C    | 4     | 15 x 2 x 2     | Side Beams|
|Assorted plywood sheets| | | to attach technical hardware to| 

If you are making your own (to work with a different drop box) you need to ensure that the frame will fit inside your box but also that all components will fit inside the box as well.

#### Raspberry Pi  
The Raspberry Pi 5 is a powerful, compact single-board computer designed to deliver significant performance improvements over previous models. Featuring a faster processor, enhanced connectivity options, and support for dual 4K displays, it is ideal for a wide range of projects, from education and DIY electronics to professional-grade embedded systems.

For further Raspberry Pi setup instructions please refer to [this guide](misc/raspberrypi_setup.md).

##### Features:

* 2.4GHz quad-core 64-bit Arm Cortex-A76 CPU
* 8GB SDRAM
* Access to common external Pi 5 ports including GPIO, 2 x USB 3.0, 2 x USB 2.0 and Gigabit Ethernet
* Dual 4Kp60 micro-HDMI display output
* PCIe 2.0 support for high-speed peripherals

---

#### Lidar 
The Garmin Lidar Lite v3 is a compact, high-performance optical distance measurement sensor solution. The lidar will be connected to the Raspberry Pi through its wiring harness:

| Wire Color | Function |
| ---------- | -------- |
| Red | 5 Vdc (+) |
| Green | I2C SCL |
| Blue | I2C SDA |
| Black | Ground (-) |

For the specific pins, refer to the Wiring Connections section. Note that the harness also has an orange wire and a yellow wire, but these are not needed and should **not** be connected to the Raspberry Pi.

For further information or to troubleshoot, see the [Operation Manual](https://static.garmin.com/pumac/LIDAR_Lite_v3_Operation_Manual_and_Technical_Specifications.pdf).

---
#### Reset Button 
The Pi Supply Digital Push Button Brick is a sensor which detects when you press the button.

The big button module pin definitions are as follows: (1) Output, (2) VCC, and (3) GND. 

To ensure the *Smart Drop-Box Frame* is able to detect when the button is pressed ensure the button output is connected to GPIO17 (Pin No. 11), VCC is connected to a 3.3V pin, and GND is connected to a GND  pin on the Raspberry Pi. For help locating the pins see the [Raspberry Pi Pinout guide](#Raspberry-Pi-Pinout).

---
#### Cameras

The *Smart Drop-Box Frame* uses two Raspberry Pi cameras (Raspberry Pi Camera 3 and Raspberry Pi Camera 3 Wide) to capture images of ballots as they are deposited. This helps provide evidence of deposited ballots and supports secure verification.

##### Camera Models:
- **Top Camera**: Raspberry Pi Camera 3   
  - Connected to **Camera Port 1** on the Raspberry Pi 5
  - Focused on obtaining a direct image of the ballot 

- **Bottom Camera**: Raspberry Pi Camera 3 Wide
  - Connected to **Camera Port 0** on the Raspberry Pi 5  
  - Captures a wider field of view to cover more of the ballot entrance area

##### Camera Setup:
- Cameras connect via the orange ribbon cables directly to the Pi 5’s CSI (Camera Serial Interface) ports.
- Both cameras are triggered nearly simultaneously using the Picamera2 library.
- Images are saved automatically as timestamped filenames in the images directory: `images/{timestamp}_{name}.jpg`
- Dual camera setup allows flexibility in capturing ballots regardless of angle or movement during deposit.

##### Notes:
- The system currently captures a picture from each camera when a ballot is detected by the Lidar or Light Curtain system.
- Minor timing adjustments (small delays between top and bottom camera capture) may be used to improve image accuracy based on how ballots fall.
- The top camera (Wide) reduces blind spots near the edges of the ballot chute.
For more information on the Raspberry Pi Camera 3 Series, refer to the [official Raspberry Pi Camera documentation](https://www.raspberrypi.com/documentation/accessories/camera.html).
---


#### E-ink display
The E-ink is a 2.13 inch e-Paper is an Active Matrix Electrophoretic Display (AMEPD), with interface and a reference system design. The 2.13” active area contains 250×122 pixels, and has 1-bit B/W full display capabilities. An integrated circuit contains gate buffer, source buffer, interface, timing control logic, oscillator, DC-DC. SRAM.LUT, VCOM and border are supplied with each panel.


##### WARNINGS AND PRECAUTIONS:
- The display glass may break when it is dropped or bumped on a hard surface. 
    Handle with care. Should the display break, do not touch the electrophoretic material.
    
    - The display module should not be exposed to harmful gases, such as acid and alkali gases, 
    which corrode electronic components.
    
    - IPA solvent can only be applied on active area and the back of a glass. 
    For the rest part, it is not allowed.
    
    - It's recommended that you consider the mounting structure so that uneven force is not applied to the module.
    
    - It's recommended that you attach a transparent protective plate to the surface in order to protect the EPD. 
    Transparent protective plate should have sufficient strength in order to resist external force.
    
    - You should adopt radiation structure to satisfy the temperature specification.
    
    - Do not touch, push or rub the exposed PS with glass, tweezers or anything harder than HB pencil lead.
    
    - When the surface becomes dusty, please wipe gently with absorbent cotton.
    
    - Wipe off water drops as soon as possible. Long time contact with PS causes deformations and color fading.
      
    【Working conditions for 240 hours】Temperature range: 0-50°C (Seven-color screen: 15-35°C); Humidity range: 35%-65%RH.
    【Storage conditions】Temperature range: below 30°C; Humidity range: below 55%RH; Maximum storage time: 6 months.
    【Transportation conditions】Temperature range: -25-70°C; Maximum transportation time: 10 days.
    【After unpacking】Temperature range: 20°C±5°C; Humidity range: 50±5%RH; Maximum storage time: Assemble within 72 hours
    
    - High temperature, high humidity, sunlight or fluorescent light may degrade the EPD panel’s performance.
    
    - When the screen is not refreshed, please set the screen to sleep mode or power off it. 
    Otherwise, the screen will remain in a high voltage state for a long time, which will damage the e-Paper and cannot be repaired!
    
    - When using the e-Paper display, it is recommended that the refresh interval is at least 180s, and refresh at least once every 24 hours. 
    If the e-Paper is not used for a long time, you should use the program to clear the screen before storing it.
    
    - The FPC cable of the screen is fragile. 
    Do not bend the cable along the vertical direction of the screen to avoid tearing the cable; 
    Avoid excessive bending line to avoid line fracture
    Do not bend the cable toward the front of the screen to prevent the cable from being disconnected from the panel.

    

##### Hardware Connection with E-ink and Raspberry Pi:
When connecting the Raspberry Pi, you can directly insert the board into the 40PIN pin header of the Raspberry Pi, and pay attention to the correct pins.
If you choose to connect with an 8PIN cable, please refer to the pin correspondence table below:
<img width="716" alt="Screenshot 2025-02-16 at 9 35 26 AM" src="https://github.com/user-attachments/assets/d1315eb7-654d-4b21-bcb7-81ece7e6b660" />



When designing the driver board, the rated input voltage of the e-Paper screen is 2.3~3.6V. If it is a 5V system, level conversion is required. In addition, the voltage should not be lower than 2.5V, so as not to affect the display effect of the e-Paper screen.
The e-Paper screen uses the cable socket 0.5-XXpin rear-flip 2.0H (FPC connector).
All screens have built-in temperature sensors, and you can use IIC pin external LM75 temperature sensor.

##### Enabling SPI Interface:
In Raspberry Pi terminal enter the following in the config interface:

    sudo raspi-config
Then:

    Choose Interfacing Options -> SPI -> Yes Enable SPI interface

Reboot Raspberry Pi:
    
    sudo reboot
    
Check /boot/config.txt, and you can see 'dtparam=spi=on' was written in as pictured below:
<img width="718" alt="Screenshot 2025-02-16 at 9 36 07 AM" src="https://github.com/user-attachments/assets/aa5a27c2-edaf-40b9-89ec-b7e59326200d" />



To make sure SPI is not occupied, it is recommended to close other drivers' coverage. You can use ls /dev/spi* to check whether SPI is occupied. If the terminal outputs /dev/spidev0.1 and /dev/spidev0.1, SPI is not occupied.
<img width="452" alt="Screenshot 2025-02-16 at 9 36 30 AM" src="https://github.com/user-attachments/assets/4a41e320-bf94-4ce4-8e20-580ca8e699f0" />


##### Python and E-ink:
While using the E-ink, in order to work in Python the following requirements must be met.
Install the function library:
    
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo apt-get install python3-numpy
    sudo pip3 install spidev

Install gpiozero library (it is installed in the system by default, if not, you can install it by following the commands below)

    sudo apt-get update
    sudo apt install python3-gpiozero

---
## Setting up the components
This guide provides step-by-step instructions to set up a Raspberry Pi with a button, an e-ink display, and a lidar sensor.
### Wiring Connections
| Pin | Connection    | Color  | -   | Pin | Connection    | Color  |
| --- | ------------- | ------ | --- | --- | ------------- | ------ |
| 1   | E-Ink VCC     | Gray   |     | 2   |               |        |
| 3   | Lidar I2C SDA | Blue   |     | 4   | Lidar VDC (+) | Red    |
| 5   | Lidar I2C SCL | Green  |     | 6   | Lidar Ground  | Black  |
| 7   |               |        |     | 8   |               |        |
| 9   | E-Ink GND     | Red    |     | 10  |               |        |
| 11  | E-Ink RST     | White  |     | 12  |               |        |
| 13  | Button S      | White  |     | 14  |               |        |
| 15  |               |        |     | 16  |               |        |
| 17  | Button V      | Red    |     | 18  | E-Ink BUSY    | Purple |
| 19  | E-Ink DIN     | Blue   |     | 20  |               |        |
| 21  |               |        |     | 22  | E-Ink DC      | Green  |
| 23  | E-Ink CLK     | Yellow |     | 24  | E-Ink CS      | Orange |
| 25  | Button G      | Black  |     | 26  |               |        |
| 27  |               |        |     | 28  |               |        |
| 29  |               |        |     | 30  |               |        |
| 31  |               |        |     | 32  |               |        |
| 33  |               |        |     | 34  |               |        |
| 35  |               |        |     | 36  |               |        |
| 37  |               |        |     | 38  |               |        |
| 39  |               |        |     | 40  |               |        |


### Ballot Collection and Verification Guide:
When the collection team arrives at the drop box location the collectors should follow the steps outlined below:
Steps:
1. Open the drop box.
2. (Both collectors independently) Verify the ballot count indicated on the drop box E-ink display.
3. Log the ballot count.
4.  (Both collectors independently)hand count the ballots
5. Compare the hand counts with the counter log entered previously. If the counts match skip to step 7.
6. Hit the reset button.
7. Close the box.
8. If the numbers did not match, send a message to the office with the disparity between counts so the office can examine the photo and scan data to determine what caused the error.



---


### Glossary:

GPIO: General-Purpose Input-Output, a set of pins that can send or receive electric signals.

---

### Diagrams and Visual Aids:
#### E-ink Display
Normal Flow
<img width="336" alt="Screenshot 2025-02-16 at 9 37 09 AM" src="https://github.com/user-attachments/assets/133cd33a-791a-4c92-a6de-0ff5f431c6ca" />

<img width="713" alt="Screenshot 2025-02-16 at 9 37 41 AM" src="https://github.com/user-attachments/assets/2984cce8-3527-4f15-8295-6f3f4f7fabb9" />


#### Raspberry Pi Pinout
<img width="476" alt="Screenshot 2025-02-16 at 9 38 28 AM" src="https://github.com/user-attachments/assets/3317b3af-258d-481e-a88d-8e0fe428a529" />

Source: pinout.xyz

---
