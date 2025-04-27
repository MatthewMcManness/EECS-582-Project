# Raspberry Pi Setup Guide

## What You'll Need

- Raspberry Pi 500
- A power supply (5V/5A)
- MicroSD card (32 GB)

## Installing the Operating System

1. Downlaod [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

2. Make sure you're connected to a stable Wi-Fi, then launch Raspberry Pi Imager

3. Click **Choose Device** and select **Raspberry 5**

4. Click **Choose OS** and select **Raspberry Pi OS (64-bit)**

5. Connect the MicroSD card to your computer. Click **Choose Storage** and select your MicroSD card.

6. Click **Next**

7. Imager will ask you to apply OS Customisation

   - Click **Edit Settings**
   - Enable **Set hostname** and set it to **RPi25**
   - Enable **Set username and password** and set it
     - For example, set username to _T25_ and password to _Capstone!582_
   - Enable **Configure wireless LAN** and change **Wireless LAN country** to **US**
     - Note that SSID and Password should fill automatically
   - Enable **Set locale settings**, this should autofill
   - Under Services, enable SSH and select **Use password authentication**
   - Under Options, enable **Eject media when finished** and **Enable telemetry**
   - Click **Save**

8. Click **Yes**

9. Click **Yes** again

10. Wait for writing to finish, a write successful message should appear, click **Continue**

11. Remove MicroSD card and connect it to the Raspberry Pi

## Connecting Other Hardware to the Raspberry Pi

Connect hardware as follows while the Raspberry Pi is powered off.

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

_Note:_ you **don't** need to connect Lidar's Mode Control nor Power Enable (the yellow and orange pin connections). For more information refer to the [lidar manual](https://cdn.sparkfun.com/assets/f/e/6/3/7/PM-14032.pdf).

## Remoting into the Raspberry Pi

We recommend using VSCode's Remote Explorer.
Note: you must be connected to the same Wi-Fi entered in the customization menu from _Installing the Operating System_

1. Open the Remote Explorer from the side panel

2. Click on **New Remote** (+)

3. Type the follong SSH command into the prompt using the username and hostname from part 7 in _Installing the Operating System_

   ```bash
   ssh <username>@<hostname>.local
   ```

   For example: `ssh T25@RPi25.local`

4. Hit Enter

5. Select SSH configuration file

   - For example: _C:\ProgramData\magaly\.ssh\config_

6. The hostname should now appear in the Remote Explorer Panel, hover over it and click **Connect in Current Window...** or **Connect in New Window...**

7. Select **Linux** as the platform

8. Enter the password from part 7 in _Installing the Operating System_
   - For example: _Capstone!582_

## Installing Requirements and Enabling SPI Interface

1. Open VSCode and open a terminal by clicking **View->Terminal**

2. Navigate to the Documents directory

   ```bash
   cd Documents
   ```

3. Install pip, pil, numpy, spidev, gpiozero, and smbus2

   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   sudo apt-get install python3-pil
   sudo apt-get install python3-numpy

   sudo apt update
   sudo apt install python3-spidev
   sudo apt install python3-gpiozero
   sudo apt install smbus2
   ```

4. Clone the Waveshare EPD Library and install it

   ```bash
   git clone https://github.com/waveshare/e-Paper
   cd e-Paper/RaspberryPi_JetsonNano/python
   sudo python3 setup.py install
   cd ../../..
   ```

5. Clone this repository

   ```bash
   git clone https://github.com/MatthewMcManness/EECS-582-Project.git

   ```

6. Edit Interface Options

   - Open the config menu
     ```bash
     sudo raspi-config
     ```
   - Enable the SPI Peripheral by choosing `Interface Options -> SPI -> Yes enable SPI interface`
   - Enable the I2C Peripheral by choosing `Interface Options -> I2C -> Yes enable ARM I2C interface`
   - Enable remote access to GPIO pins by choosing `Interface Options -> Remote GPIO -> Yes enable access to GPIO server over the network`
   - Exit the config menu by choosing `Finish`

7. Reboot the Raspberry Pi

```bash
sudo reboot
```

## Running Code

To run the project, in a terminal navigate to the `EECS-582-Project` directory and enter:

```bash
python3 main.py
```

To run a file in the top directory (`EECS-582-Project`), enter in a terminal:

```bash
python3 file_name.py
```

For other files that are located in sub-directories, for example `EECS-582-Project/tests/t1_with_lidar.py`:

```bash
python3 -m tests.t1_with_lidar
```
