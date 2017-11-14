from numpy import *
import matplotlib.pyplot as mp
import datetime
infile = open('distribution_ht.txt','r')
lines = [line for line in infile]
infile.close()
lines2 = []
count = 0
rownumberlines = int(len(lines)/4)
linesvec = zeros((rownumberlines, 32))
count2 = 0

for line in lines:
    number_str = line.split()
    numbers = [float(w) for w in number_str]
    if numbers[0] > 10000:
        count2 = 0
        for i in range(len(numbers)):
            linesvec[count][count2] = numbers[i]
            count2 += 1
        count += 1
    else:
        for i in range(len(numbers)):
            linesvec[count-1][count2] = numbers[i]
            count2 += 1
#print len(linesvec[:][1])

x = linspace(1,len(linesvec[200][1:]),31)

x = []
#x = zeros(len(linesvec))
y = zeros(len(linesvec))
for i in range(len(linesvec)):
    dtt = int(linesvec[i][0])
    dt = str(dtt)
    print dt

    x.append(datetime.datetime.strptime(dt,'%Y%m%d'))
    print x[i]

    y[i] = linesvec[i][10]

mp.plot(x,y, 'r*')
#mp.plot(linesvec[200][1:],x)

mp.show()
