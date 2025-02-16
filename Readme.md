# User Guide for the "Smart Drop-Box Frame"

## System Overview:

### Matthew

## Component Guide:

### Raspberry Pi -- Mariam 
The Raspberry Pi 500 is a fast, powerful computer integrated into a high-quality keyboard, delivering the ultimate compact PC experience. Equipped with the same quad-core 64-bit Arm processor and RP1 I/O controller as the Raspberry Pi 5, it also includes a built-in aluminum heatsink for enhanced thermal performance. This ensures smooth operation even under heavy workloads while supporting stunning dual 4K display output.

#### Features

* 2.4GHz quad-core 64-bit Arm Cortex-A76 CPU
* 8GB SDRAM
* Built in aluminum heat sink
* Sleek form factor
* Access to common external Pi 5 ports including GPIO, 2 x USB 3.0, 1 x USB 2.0 and Gigabit Ethernet

### Light Curtain -- Mariam
A light curtain is a safety device used in industrial automation to detect objects. It consists of an array of infrared light beams emitted from a transmitter and received by a receiver. When a beam is interrupted, the system triggers a response, which indicates it detected an object.

The light curtain sensor responds as fast as 0.01 seconds. And the detection distance between transmitter and receiver can be up to 5m.


### Reset Button -- Magaly
The Pi Supply Digital Push Button Brick is a sensor which detects when you press the button.

The big button module pin definitions are as follows: (1) Output, (2) VCC, and (3) GND. 

To ensure the *Smart Drop-Box Frame* is able to detect when the button is pressed ensure the button output is connected to GPIO17 (Pin No. 11), VCC is connected to a 3.3V pin, and GND is connected to a GND  pin on the Raspberry Pi. For help locating the pins see the [Raspberry Pi Pinout guide](#Raspberry-Pi-Pinout).

### E-ink -- Ashley and Manvir
The E-ink is a 2.13 inch e-Paper is an Active Matrix Electrophoretic Display (AMEPD), with interface and a reference system design. The 2.13” active area contains 250×122 pixels, and has 1-bit B/W full display capabilities. An integrated circuit contains gate buffer, source buffer, interface, timing control logic, oscillator, DC-DC. SRAM.LUT, VCOM and border are supplied with each panel.

#### WARNINGS AND PRECAUTIONS
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
      
    【Working conditions for 240 hours】Temperature range: 0~50°C (Seven-color screen: 15~35°C); Humidity range: 35%~65%RH.
    【Storage conditions】Temperature range: below 30°C; Humidity range: below 55%RH; Maximum storage time: 6 months.
    【Transportation conditions】Temperature range: -25~70°C; Maximum transportation time: 10 days.
    【After unpacking】Temperature range: 20°C±5°C; Humidity range: 50±5%RH; Maximum storage time: Assemble within 72 hours.
    
    - High temperature, high humidity, sunlight or fluorescent light may degrade the EPD panel’s performance.
    
    - When the screen is not refreshed, please set the screen to sleep mode or power off it. 
    Otherwise, the screen will remain in a high voltage state for a long time, which will damage the e-Paper and cannot be repaired!
    
    - When using the e-Paper display, it is recommended that the refresh interval is at least 180s, and refresh at least once every 24 hours. 
    If the e-Paper is not used for a long time, you should use the program to clear the screen before storing it.
    
    - The FPC cable of the screen is fragile. 
    Do not bend the cable along the vertical direction of the screen to avoid tearing the cable; 
    Avoid excessive bending line to avoid line fracture
    Do not bend the cable toward the front of the screen to prevent the cable from being disconnected from the panel.

#### Hardware Connection with E-ink and Raspberry Pi
When connecting the Raspberry Pi, you can directly insert the board into the 40PIN pin header of the Raspberry Pi, and pay attention to the correct pins.
If you choose to connect with an 8PIN cable, please refer to the pin correspondence table below:
![Screenshot 2025-02-15 at 5.30.26 PM](https://hackmd.io/_uploads/HJNCQs0KJe.png)

</br>

When designing the driver board, the rated input voltage of the e-Paper screen is 2.3~3.6V. If it is a 5V system, level conversion is required. In addition, the voltage should not be lower than 2.5V, so as not to affect the display effect of the e-Paper screen.
The e-Paper screen uses the cable socket 0.5-XXpin rear-flip 2.0H (FPC connector).
All screens have built-in temperature sensors, and you can use IIC pin external LM75 temperature sensor.

#### Enabling SPI Interface
In Raspberry Pi terminal enter the following in the config interface:

    sudo raspi-config
Then:

    Choose Interfacing Options -> SPI -> Yes Enable SPI interface

Reboot Raspberry Pi:
    
    sudo reboot
    
Check /boot/config.txt, and you can see 'dtparam=spi=on' was written in as pictured below:
![Screenshot 2025-02-15 at 5.42.04 PM](https://hackmd.io/_uploads/SJT28oCtJx.png)


To make sure SPI is not occupied, it is recommended to close other drivers' coverage. You can use ls /dev/spi* to check whether SPI is occupied. If the terminal outputs /dev/spidev0.1 and /dev/spidev0.1, SPI is not occupied.
![Screenshot 2025-02-15 at 5.42.31 PM](https://hackmd.io/_uploads/rJiiUo0Kyg.png)

#### Python and E-ink
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

</br>

## Ballot Collection and Verification Guide:

### Matthew

## Glossary:
### Add what you need 
GPIO
: General-Purpose Input-Output, a set of pins that can send or receive electric signals.

## Troubleshooting Guide:
### Not ready to do

## Diagrams and Visual Aids:
### Add anything here you add to your section
### E-ink Display
Normal Flow
![image](https://github.com/user-attachments/assets/bff06cc4-f224-44ad-81fc-257aab567394)



### Raspberry Pi Pinout
![image](https://github.com/user-attachments/assets/56a5bc1b-0321-4a22-9ba3-78a4c3da06f1)

Source: pinout.xyz
