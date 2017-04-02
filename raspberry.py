from math import radians, cos, sin, asin, sqrt
import re
import time
import datetime
import threading
import serial
import os


GPS_port = '/dev/ttyAMA0'
arduino_port = '/dev/pts/2' # /dev/ttyUSB1

if not os.path.exists("data"):
    os.makedirs("data")


class GPSListener:

    def __init__(self):
        self.thread = threading.Thread(target=self.receive, name="GPS-listener-Thread")
        self.lat = 0
        self.lon = 0
        self.speed = 0
        self.start_time = 0
        self.gps_module = serial.Serial(GPS_port, 9600)
        self.answer = []
        self.satelites = 0
        self.speed_gps = 0
        self.altitude = 0

    def parse_gps_string(self, str0):
        _lat_in, _latD_in, _lon_in, _lonD_in, _, self.satelites, acc, self.altitude = str0.strip().split(',')[2:10]

        _tmp = _lat_in.split('.')[1]
        _tmp_0 = _tmp[len(_tmp)-3:len(_tmp)]
        _tmp_1 = _tmp[0:len(_tmp)-3]
        _tmp_last = str(_tmp_1)+"."+str(_tmp_0)

        _tmp = _lat_in.split('.')[0]
        _tmp_0 = _tmp[len(_tmp)-2:len(_tmp)]
        _tmp_1 = _tmp[0:len(_tmp)-2]
        _tmp_first = str(_tmp_1)+" "+str(_tmp_0)+"'"
        _lat = _tmp_first + " " + _tmp_last

        _tmp = _lon_in.split('.')[1]
        _tmp_0 = _tmp[len(_tmp)-3:len(_tmp)]
        _tmp_1 = _tmp[0:len(_tmp)-3]
        _tmp_last = str(_tmp_1)+"."+str(_tmp_0)

        _tmp = _lon_in.split('.')[0]
        _tmp_0 = _tmp[len(_tmp)-2:len(_tmp)]
        _tmp_1 = _tmp[0:len(_tmp)-2]
        _tmp_first = str(_tmp_1)+" "+str(_tmp_0)+"'"
        _lon = _tmp_first + " " + _tmp_last

        parts = re.split('[^\d\w]+', _lat)
        _lat = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / (60 * 60)

        parts = re.split('[^\d\w]+', _lon)
        _lon = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / (60 * 60)

        def _distance(lon1, lat1, lon2, lat2):

            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            km = 6367 * c

            if km > 1000: km = 0
            return km
        
        _speed = (_distance(self.lon, self.lat, _lon, _lat)*(time.time()-self.start_time)) * 3600

        self.lon = _lon
        self.lat = _lat
        return _lat, _lon, round(_speed, 2)

    def receive(self):
        self.answer = []
        while True:
            for cc in self.gps_module.read():
                self.answer.append(chr(cc))
                joined_string = ''.join(str(v) for v in self.answer)

                if chr(cc) == '\n':
                    d = joined_string.replace('\n', '')
                    d = d.replace('\r', '')
                    if d.startswith('$GPGGA'):
                        self.start_time = time.time()
                        self.lat, self.lon, self.speed = self.parse_gps_string(d)
                    elif d.startswith('$GPRMC'):
                        self.speed_gps = round(float(d.strip().split(',')[7]) * 1.852, 2)
                    self.answer = []
                break

    def start(self):
        self.thread.start()

    def gps(self):
        return [self.lat, self.lon, self.speed, self.speed_gps, self.satelites, self.altitude]


gps_class = GPSListener()
gps_class.start()

arduino_serial = serial.Serial(arduino_port, 9600)
filename = "data/" + datetime.datetime.now().strftime("%d_%m_%Y_%H_%M") + ".txt"
answer = []


while True:
    with open(filename, 'a') as out:
        for c in arduino_serial.read():
            answer.append(chr(c))
            joined_seq = ''.join(str(v) for v in answer)

            if chr(c) == '\n':
                joined_seq = joined_seq.replace('\n', '')
                joined_seq = joined_seq.replace('\r', '')
                gps_values = gps_class.gps()
                data = joined_seq
                date = datetime.datetime.now().strftime("%H:%M:%S:%f")
                values = re.split(',', data)
                values.append(gps_values)
                values.append(date)

                out.write(str(values) + "\n")
                print(values)
                answer = []
            break
