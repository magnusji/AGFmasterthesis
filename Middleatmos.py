from numpy import *
import datetime
import matplotlib.pyplot as mp
import scipy.stats as stats
from nrlmsise_00_header import *
from nrlmsise_00 import *

from scipy import exp, asarray as ar
from scipy.optimize import curve_fit


class Middleatmos:

    def readoh(self,filename):
        '''
        This function reads OH data from file to a matrix OH_data
        Needs input filename of OH data,
        '''

        self.filename = filename

        infile = open(self.filename, 'r')
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

    def gaus(self,x,a, x0,sigma): #making a gaussian function to use in fitting
        '''
        Gaussian function, taking the inputs x,a,x0 and sigma.
        x is the height column,
        a is a constant 1,
        x0 is the mean position of the bell curve_fit,
        sigma^2 is the variance to the function
        '''
        return a*exp(-((x-x0)**2.0)/(2.0*sigma**2.))

    def gaussian(self,Sdata, Datefit, i, N, x): #input data for a distribution Susydat[i][1:]
        '''
        Fitting the data points to the gaussian function gaus
        Input Sdata is the distribution of the column,
        given by the suzy radar data.
        Takes Sdata, Datefit,i,N,x
        Sdata: is the distribution data from the suzy radar
        Datefit: The date from which the data is taken
        i: the iteration number, how far along the line of the dateset it is,
        N: Length of data sting sent in to the function
        x: vector giving the height distribution of Sdata
        These should be computed outside to prevent mismatch
        '''
         #defining the height
        y = ar(Sdata) #making sure the data set is an array
        if sum(y)>=1.0:
            mean = float(sum(x*y)/sum(y)) #finding the average value (center of the curve)
            sigma = sqrt(sum((y*(x-mean)**2.)/sum(y))) #variance for the gauss function
            if sigma == 0:
                print('Error no fit to function, date = %i, number in line i = %i' %(Datefit, i))
                y_fit = zeros(N)
            else:
                try:
                    popt,pcov = curve_fit(self.gaus,x,y,p0=[1,mean,sigma], maxfev=1000)
                    y_fit = ar(self.gaus(x,*popt))
                except RuntimeError:
                    print('Error - curve_fit failed, date = %i, number in line i = %i'%(Datefit, i))
                    y_fit = zeros(N)

        else:
            y_fit = zeros(N)
        return x,y_fit #returns x as height and y_fit as the fitted number of occurances


    def sort_suzy(self, Suzy_data, ap_f107):
        '''
        Sorting the maximum # of meteor burnouts for height
        returns
            susyx_x: raw date yyyymmdd
            susyx: datetime format of the datetime
            susyy: the maximum height of the fitted curve
            susyy_b: The raw height maximum number of occurances (without fit)
            tempyy: the temperatures found using the model without the AP an F10.7 data
            tempyy_ap: the tempersture foung when giving the ap and F10.7 data to the model
        '''
        Susydat = Suzy_data
        ap_data = ap_f107
        susyx = []
        #x = zeros(len(linesvec))

        susyx_x = zeros(len(Susydat))
        susyy = zeros(len(Susydat))
        susyy_b = zeros(len(Susydat))
        susy_dofy = zeros(len(Susydat))
        tempyy = zeros(len(Susydat))
        tempyy_ap = zeros(len(Susydat))
        for i in range(len(Susydat)):
            dtt = int(Susydat[i][0])
            susyx_x[i] = dtt
            dt = str(dtt)
            susyx.append(datetime.datetime.strptime(dt,'%Y%m%d'))
            d2tt = datetime.datetime.strptime(dt,'%Y%m%d')
            d2t = int(datetime.date.strftime(d2tt,'%j'))
            year2t = int(datetime.date.strftime(d2tt,'%Y'))

            '''
            Making a nested loop to find values for Ap and F10.7,
            for dates corresponding to the given dates for the season
            '''
            for j in range(len(ap_data)):
                if int(ap_data[j][0]) == year2t: # testing for year
                    if int(ap_data[j][1]) == d2t: # testing for DOY
                        ap_j = ap_data[j][4] # Daily ap average
                        f107_j = ap_data[j-1][5] # using F10.7 daily average from previous day
                        f107_81avg_a = 0
                        counter_f107 = 0
                        if j>42 or j<(len(ap_data)-42):
                            for l in range(j-41 ,j+40): #Finding the 81 day average solar flux F10.7, requires F10.7 data for 42 days before and after wanted date
                                f107_81avg_a += ap_data[l][5]
                                counter_f107 += 1
                                f107_81avg = f107_81avg_a/counter_f107 #The 81 day avg of F10.7
                        else:
                            f107_81avg = 150
                        #print(f107_81avg, counter_f107  ) #checking the calculations
            Sdata = Susydat[i][1:]
            N = len(Sdata)
            x = ar(linspace(70.0,100.0,N))
            x,y_fit= self.gaussian(Sdata, dtt, i,N, x)
            susyy[i] = x[y_fit.argmax()]
            tempyy[i] = self.amod_nrlmsise_00(d2t,susyy[i]) #d2t=DOY, Susyy=altitude
            #print (tempyy)
            tempyy_ap[i] = self.amod_nrlmsise_00(d2t,susyy[i],ap_j, f107_j,f107_81avg)
            susyy_b[i] = x[Sdata.argmax()]
            '''
            for j in range(len(Susydat[i][1:])):
                if Susydat[i][j+1] > testx:
                    testx = Susydat[i][j+1]
                    x = j+1
                susyy[i] = x + 70  #susyy is from the height 70-100 km so need to add 69 in order to convert
            '''
            #altitudex = susyy[i]

        return susyx_x, susyx, susyy, susyy_b, tempyy, tempyy_ap


    def read_kp_ap(self,filename_kp):
        '''
        Reads kp and ap data from file Kp_****.dat
        Not currently in use, due to finding ap data in better format
        '''

        infile = open(filename_kp,'r')
        infile.readline()
        Lines = [line for line in infile]
        infile.close()
        N = len(Lines)
        #print(Lines)
        print(N)
        counter = 0
        kp_data = zeros((N, 19))
        ap = zeros((N,2))
        for line in Lines:
            for char in '+-':
                line = line.replace(char,' ')
            words = line.split()
            numbers = [float(w) for w in words]
            #print(numbers)
            for i in range(len(numbers)):
                kp_data[counter][i] = numbers[i]
            ap[counter][0] = kp_data[counter][0]
            ap[counter][1] = kp_data[counter][-1]
            counter += 1
        print(kp_data[1][-1])
        #print('ap')
        print(ap)

    def omniread(self,filename):
        '''
        Reads file lst gotten from omniweb NASA, this file has specification

          FORMAT OF THE SUBSETTED FILE

            ITEMS                      FORMAT

         1 YEAR                          I4
         2 DOY                           I4
         3 Hour                          I3
         4 Scalar B, nT                  F6.1
         5 ap_index, nT                  I4
         6 f10.7_index                   F6.1

        This file was produced by SPDF OMNIWeb Plus service

        Sorts the different columns in the matrix omnimtx for further use
        '''
        infile = open(filename)
        lines = [line for line in infile]
        infile.close()

        omnimtx = zeros((len(lines),6))
        counter = 0
        for line in lines:
            wordstr = line.split()
            numbers = [float(w) for w in wordstr]
            for i in range(len(numbers)):
                omnimtx[counter][i] = numbers[i]
            counter += 1
        return omnimtx


    def amod_nrlmsise_00(self, doy,alt, ap=4.0, f107=150,f107A=150):

        import time


        dayofyear = doy
        altitude = alt
        output = nrlmsise_output()
        Input = nrlmsise_input()
        flags = nrlmsise_flags()
        aph = ap_array()

        for i in range(7):
            aph.a[i]=100
        flags.switches[0] = 0
        for i in range(1, 24):
            flags.switches[i]=1


        Input.doy=dayofyear;
        Input.year=0; #/* without effect */
        Input.sec=3600; # at 1 UTC
        Input.alt= altitude; # This will vary
        Input.g_lat=78; # latitude of interest
        Input.g_long=20; # longitude of interest
        Input.lst=4; # local standard time
        Input.f107A=f107A; #81 day average around date, should be set to 150
        Input.f107=f107; # previous day f10.7, should be set to 150
        Input.ap= ap; #magnetic activity, should be set to 4


        #evaluate 0 to 14

        gtd7(Input, flags, output)

        return output.t[1]

    def seasons(self,susyx,oh_time,Suzy_data='NO'):
        '''
        Sorts out indexes of Suzydata in order to match the season of interest,
        using the time stamps of the OH seasonal data to find matching times in the Suzy data.
        Takes
        Susyx: the time series from Suzydata,
        oh_time: OH seasonal timeseries

        returns
        Seasonal dates as datetime objects
        Seasonal indicies
        Seasonal data for input Suzy_data

        '''
        susy_time = susyx
        suzydata = Suzy_data

        oh_time = oh_time
        within = []
        withininx = []
        indexcounter = 0
        for date in susy_time:
            if oh_time[0] < date <oh_time[-1]:
                withininx.append(indexcounter)
                within.append(date)
            indexcounter += 1
        #print(withininx)
        #print(len(within))
        if suzydata == 'NO':
            return within,withininx
        else:
            seasonalsuzy = suzydata[withininx]
            return within,withininx, seasonalsuzy

    def seasonsplot_temperature(self,seasonaldates,seasonalsuzy,seasonaltemperature,OH_dates,OH_temperature):

        mp.figure()
        ax1 = mp.subplot(211)
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonaltemperature,'ro:', label='Meteor')

        l2 =ax2.plot(OH_dates, OH_temperature,'bo--', label='OH')

        ax1.set_ylabel('[$^o$K] Temperature at maximum meteor burnout')
        #ax1.set_ylim(210,235)
        ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')
        #ax2.set_ylim(170,250)
        lns = l1 +l2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns,labs,loc=0)
        mp.subplot(212)
        mp.plot(seasonaldates,seasonalsuzy, 'ro:')
        mp.ylabel('[km] Height meteor burnout')
        mp.ylim(70,100)
        mp.gcf().autofmt_xdate()

    def seasonsplot_temperature_ap(self,seasonaldates,seasonalsuzy,seasonaltemperature,seasonaltemperature_ap,OH_dates,OH_temperature):

        mp.figure()
        ax1 = mp.subplot(211)
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonaltemperature,'ro:', label='Meteor')

        l2 =ax2.plot(OH_dates, OH_temperature,'bo--', label='OH')
        l3 = ax1.plot(seasonaldates,seasonaltemperature_ap, 'go:', label='Meteor_AP')

        ax1.set_ylabel('[$^o$K] Temperature at maximum meteor burnout')
        #ax1.set_ylim(210,235)
        ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')
        #ax2.set_ylim(170,250)
        lns = l1 +l2 + l3
        labs = [l.get_label() for l in lns]
        ax1.legend(lns,labs,loc=(1.04,1))
        mp.subplot(212)
        mp.plot(seasonaldates,seasonalsuzy, 'ro:')
        mp.ylabel('[km] Height meteor burnout')
        mp.ylim(70,100)
        mp.gcf().autofmt_xdate()


    def seasonsplot_height(self,seasonaldates,seasonalsuzy,OH_dates,OH_temperature):

        fig,ax1 = mp.subplots()
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonalsuzy,'ro', label='suzy')

        l2 =ax2.plot(OH_dates, OH_temperature,'bo')
        ax1.set_ylim(70,100)
        fig.autofmt_xdate()
        ax1.set_ylabel('[Km] Height of maximum meteor burnout')
        ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')

        return linesvec


class Read_four_lines:

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
