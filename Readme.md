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
The Raspberry Pi 500 is a fast, powerful computer integrated into a high-quality keyboard, delivering the ultimate compact PC experience. Equipped with the same quad-core 64-bit Arm processor and RP1 I/O controller as the Raspberry Pi 5, it also includes a built-in aluminum heatsink for enhanced thermal performance. This ensures smooth operation even under heavy workloads while supporting stunning dual 4K display output.

##### Features:

* 2.4GHz quad-core 64-bit Arm Cortex-A76 CPU
* 8GB SDRAM
* Built in aluminum heat sink
* Sleek form factor
* Access to common external Pi 5 ports including GPIO, 2 x USB 3.0, 1 x USB 2.0 and Gigabit Ethernet

---

#### Light Curtain 
A light curtain is a safety device used in industrial automation to detect objects. It consists of an array of infrared light beams emitted from a transmitter and received by a receiver. When a beam is interrupted, the system triggers a response, which indicates it detected an object.

The light curtain sensor responds as fast as 0.01 seconds. And the detection distance between transmitter and receiver can be up to 5m.

---
#### Reset Button 
The Pi Supply Digital Push Button Brick is a sensor which detects when you press the button.

The big button module pin definitions are as follows: (1) Output, (2) VCC, and (3) GND. 

To ensure the *Smart Drop-Box Frame* is able to detect when the button is pressed ensure the button output is connected to GPIO17 (Pin No. 11), VCC is connected to a 3.3V pin, and GND is connected to a GND  pin on the Raspberry Pi. For help locating the pins see the [Raspberry Pi Pinout guide](#Raspberry-Pi-Pinout).

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
This guide provides step-by-step instructions to set up a Raspberry Pi with a button, an e-ink display, and a light curtain sensor.
### Wiring Connections
#### Button Connection
| Button Pin | Raspberry Pi Pin |
| -------- | -------- | 
| GND (G)  |Pin 39 (GND)   | 
| VCC (V)   | Pin 4 (5V)   | 
| Output (S)  | Pin 13 (GPIO 27)    | 

#### E-Ink Display Connection
| E-Ink Pin | Raspberry Pi Pin |
| -------- | -------- | 
| VCC  |Pin 2 (5V)   | 
| GND   | Pin 6 (GND)   | 
| DIN  | Pin 19 (GPIO 10, SPI0 MOSI)   | 
| CLK | Pin 23 (GPIO 11, SCLK) |
| CS | Pin 24 (GPIO 8, SPI0 CE0) |
| DC | Pin 22 (GPIO 25) |
| RST | Pin 11 |
| BUSY | Pin 18 (GPIO 24) |

#### Light Curtain Connection
| Light Curtain Pin | Raspberry Pi Pin |
| -------- | -------- | 
| Signal | Pin 15 (GPIO 22) (subject to change)  |


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

### Troubleshooting Guide:
Nothing as of yet, but we will update as we go along


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
