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
        needs input filename of OH data
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


    def sort_suzy(self, Suzy_data):
        '''
        Sorting the maximum # of meteor burnouts for height
        returns
            susyx_x: raw date yyyymmdd
            susyx: datetime format of the datetime
            susyy: the maximum height of the fitted curve
            susyy_b: The raw height maximum number of occurances (without fit)
        '''
        Susydat = Suzy_data
        susyx = []
        #x = zeros(len(linesvec))

        susyx_x = zeros(len(Susydat))
        susyy = zeros(len(Susydat))
        susyy_b = zeros(len(Susydat))
        susy_dofy = zeros(len(Susydat))
        tempyy = zeros(len(Susydat))
        for i in range(len(Susydat)):
            dtt = int(Susydat[i][0])
            susyx_x[i] = dtt
            dt = str(dtt)
            susyx.append(datetime.datetime.strptime(dt,'%Y%m%d'))
            d2tt = datetime.datetime.strptime(dt,'%Y%m%d')
            d2t = int(datetime.date.strftime(d2tt,'%j'))

            Sdata = Susydat[i][1:]
            N = len(Sdata)
            x = ar(linspace(70.0,100.0,N))
            x,y_fit= self.gaussian(Sdata, dtt, i,N, x)
            susyy[i] = x[y_fit.argmax()]
            tempyy[i] = self.amod_nrlmsise_00(d2t,susyy[i])
            #print (tempyy)
            susyy_b[i] = x[Sdata.argmax()]
            '''
            for j in range(len(Susydat[i][1:])):
                if Susydat[i][j+1] > testx:
                    testx = Susydat[i][j+1]
                    x = j+1
                susyy[i] = x + 70  #susyy is from the height 70-100 km so need to add 69 in order to convert
            '''
            #altitudex = susyy[i]

        return susyx_x, susyx, susyy, susyy_b, tempyy


    def amod_nrlmsise_00(self, doy,alt):

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
        Input.f107A=150; #81 day average around date, should be set to 150
        Input.f107=150; # previous day f10.7, should be set to 150
        Input.ap=4; #magnetic activity, should be set to 4


        #evaluate 0 to 14

        gtd7(Input, flags, output)


        #/* output type 1 */
        '''
        print('\n', end='')
        for j in range(9):
            print('%E ' % output.d[j], end='')
        print('%E ' % output.t[0], end='')
        print("\nDAY   ", end='')

        print("         %3i" % Input.doy, end='')
        print("\nALT   ", end='')

        print("        %4.0f" % Input.alt, end='')
        print("\nTINF  ", end='')

        print("     %7.2f" % output.t[0], end='')
        print("\nTG    ", end='')

        print("     %7.2f" % output.t[1], end='')
        print("\nHE    ", end='')

        print("   %1.3e" % output.d[0], end='')
        print("\nO     ", end='')

        print("   %1.3e" % output.d[1], end='')
        print("\nN2    ", end='')

        print("   %1.3e" % output.d[2], end='')
        print("\nO2    ", end='')

        print("   %1.3e" % output.d[3], end='')
        print("\nAR    ", end='')

        print("   %1.3e" % output.d[4], end='')
        print("\nH     ", end='')

        print("   %1.3e" % output.d[6], end='')
        print("\nN     ", end='')

        print("   %1.3e" % output.d[7], end='')
        print("\nANM   ", end='')

        print("   %1.3e" % output.d[8], end='')
        print("\nRHO   ", end='')

        print("   %1.3e" % output.d[5], end='')
        print('\n')
        '''
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


        ax1 = mp.subplot(211)
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonaltemperature,'ro:', label='suzy')

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

    def seasonsplot_height(self,seasonaldates,seasonalsuzy,OH_dates,OH_temperature):

        fig,ax1 = mp.subplots()
        ax2 = ax1.twinx()
        l1 = ax1.plot(seasonaldates,seasonalsuzy,'ro', label='suzy')

        l2 =ax2.plot(OH_dates, OH_temperature,'bo')
        ax1.set_ylim(70,100)
        fig.autofmt_xdate()
        ax1.set_ylabel('[Km] Height of maximum meteor burnout')
        ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')
