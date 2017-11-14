from numpy import *
import matplotlib.pyplot as mp
import datetime

infile = open('daily_OHtemp_0203_mies.dat', 'r')
lines =[line for line in infile]
OH_data = zeros((len(lines),8))
counter = 0
for line in lines:
    words = line.split()
    numbers = [float(w) for w in words]
    for i in range(len(numbers)):
        OH_data[counter][i] = numbers[i]
    counter += 1

print OH_data

x = []
#x = zeros(len(OH_data))
y = zeros(len(OH_data))

for i in range(len(OH_data)):
    dy = int(OH_data[i][0])
    dm = int(OH_data[i][1])
    dd = int(OH_data[i][2])
    dt = datetime.datetime(dy, dm, dd)
    x.append(dt)
    #x[i] = OH_data[i][0] #needs to get format yyyymmdd
    y[i] = OH_data[i][4]

mp.plot(x,y, 'bo')
mp.show()
