# Telemetry
Simple telemetry app based on arduino and Raspberry Pi.

## Installation
You can download code by github button or:

```sh
git clone https://github.com/exelban/telemetry
```
Next copy file ```raspberry.py``` to your raspberry Pi. Dont forget to change arduino port, if its different.
For compile arduino code you must to download and install [SimpleTimer Library](http://playground.arduino.cc/Code/SimpleTimer), 
because we use it for speed calculation.
Next you can upload file ```arduino.ino``` to you arduino board.
Also i recommend to install Arduino IDE to raspberry Pi. You can do it by ```apt install arduino ```

## Usage
I use Python 3.5 so you must to compile this version (or you can change code to oldest version).
This version of code write all collected data to file (named by time) in folder data.
After you connected all sensors to arduino board and arduino board to raspberry Pi you can run ```python3 raspberry.py``` on your raspberry Pi.
Also you must to change all sensors ports in ```arduino.ino```.


## Structure
![](https://s3.eu-central-1.amazonaws.com/serhiy/Github_repo/Zrzut+ekranu+2017-03-29+o+21.26.37.png) 

Polish version (there was used radiomodem to transmit all data to computer).
![](https://s3.eu-central-1.amazonaws.com/serhiy/Github_repo/12970154_1156605494389480_584957392_o.jpg) 

## Licence
[GNU Affero General Public License](https://github.com/exelban/telemetry/blob/master/LICENSE)
