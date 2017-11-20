from numpy import *
import datetime
import matplotlib.pyplot as mp
class Read_four_lines():

    def read_suzy(self,filename):
        infile = open(filename,'r')
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
        return linesvec

    def read_oh(self,filename):
        infile = open(filename, 'r')
        lines =[line for line in infile]
        OH_data = zeros((len(lines),8))
        counter = 0
        for line in lines:
            words = line.split()
            numbers = [float(w) for w in words]
            for i in range(len(numbers)):
                OH_data[counter][i] = numbers[i]
            counter += 1
        return OH_data

    def sort_oh(self, OH_data):
        OH_data = OH_data
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

        return x,y

    def sort_suzy(self, Suzy_data):
        '''
        Sorting the maximum # of meteor burnouts for height
        '''
        Susydat = Suzy_data
        susyx = []
        #x = zeros(len(linesvec))
        susyx_x = zeros(len(Susydat))
        susyy = zeros(len(Susydat))
        for i in range(len(Susydat)):
            dtt = int(Susydat[i][0])
            susyx_x[i] = dtt
            dt = str(dtt)
            susyx.append(datetime.datetime.strptime(dt,'%Y%m%d'))
            testx = 0
            x = 0
            for j in range(len(Susydat[i][1:])):
                if Susydat[i][j+1] > testx:
                    testx = Susydat[i][j+1]
                    x = j+1
                susyy[i] = x + 70  #susyy is from the height 70-100 km so need to add 69 in order to convert
        return susyx_x, susyx, susyy

    def single_dist_suzy(self,Suzy_data,x):
        Susydat = Suzy_data
        susyx = Suzy_data[x][1:]
        #x = zeros(len(linesvec))
        susyy = linspace(70,100,len(Susydat[x][1:]))

        return susyx, susyy

    def seasons(self,susyx,oh_time,Suzy_data, OH_data):
        susy_time = susyx
        suzydata = Suzy_data
        oh_data = OH_data
        oh_time = oh_time
        within = []
        withininx = []
        indexcounter = 0
        for date in susy_time:
            if oh_time[0] < date <oh_time[-1]:
                withininx.append(indexcounter)
                within.append(date)
            indexcounter += 1
        print(withininx)
        print(len(within))
        seasonalsuzy = suzydata[withininx]

        return within, seasonalsuzy

    def seasonsplot(self,seasonaldates,seasonalsuzy,xx,yy):

        fig,ax1 = mp.subplots()
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonalsuzy,'ro', label='suzy')

        l2 =ax2.plot(xx,yy,'bo')
        ax1.set_ylim(70,100)
        fig.autofmt_xdate()
        ax1.set_ylabel('[Km] Height of maximum meteor burnout')
        ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')
