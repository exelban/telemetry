# Telemetry
Simple telemetry app based on arduino and Raspberry Pi.

## Installation
```sh
git clone https://github.com/exelban/telemetry
```

## Usage
### Raspberry Pi
I use Python 3.5 so you must to compile this version (or you can change code for oldest version of python).

Copy file ```raspberry.py``` to your raspberry Pi.

You must to find on what port connected arduino and GPS module.<br />
In Raspberry Pi 2 dafault RX/TX port is ```/dev/ttyAMA0```. But also you must to make some changes in system files ([See here](https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi?view=all)).

When you find port just change there in raspberry.py:
```python
GPS_port = '/dev/ttyAMA0'
arduino_port = '/dev/ttyUSB1'
```

**If you dont use GPS, just leave ```GPS_port``` empty.**

### Arduino
For compile arduino code you must to download and install [SimpleTimer Library](http://playground.arduino.cc/Code/SimpleTimer), because we use it for speed calculation.

If you connected sensors to different port on arduino just change it in ```arduino.ino```.
Next upload file ```arduino.ino``` to you arduino board.

I recommend to install Arduino IDE to raspberry Pi. You can do it by print ```apt install arduino ``` in terminal.

**Dont worry if you have different sensors or use your own arduino code. Script on Raspberry Pi justt add all received data from adruino to final array.**

After you connected all sensors to arduino board and arduino board to raspberry Pi you can run ```python3 raspberry.py``` on your raspberry Pi.

## Structure
![](https://s3.eu-central-1.amazonaws.com/serhiy/Github_repo/Zrzut+ekranu+2017-03-29+o+21.26.37.png) 

Polish version (there was used radiomodem to transmit all data to computer).
![](https://s3.eu-central-1.amazonaws.com/serhiy/Github_repo/12970154_1156605494389480_584957392_o.jpg) 

## Licence
[GNU Affero General Public License](https://github.com/exelban/telemetry/blob/master/LICENSE)
