import serial
import datetime
import re

arduino = serial.Serial('/dev/ttyACM0',9600)
now_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
answer = []

print (now_date)
filename = "data/"+now_date+".txt"

while True:
	with open(filename, 'a') as out:
		for c in arduino.read():
			answer.append(chr(c))
			joined_seq = ''.join(str(v) for v in answer)
	
			if chr(c) == '\n':
				joined_seq = joined_seq.replace('\n', '')
				joined_seq = joined_seq.replace('\r', '')
				gps_values = [0, 0, 0]
				data = joined_seq
				date = datetime.datetime.now().strftime("%H:%M:%S:%f")
				values = re.split(' ', data)
				values.append(gps_values)
				values.append(date)
				
				out.write(str(values)+"\n")
				print(values)
				answer = []
				break

out.close()
