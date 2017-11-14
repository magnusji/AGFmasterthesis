from numpy import *
import datetime
import matplotlib.pyplot as mp
import scipy.stats as stats
from scipy import exp, asarray as ar
from scipy.optimize import curve_fit
class Middleatmos:

    def readoh(self,filename):
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
        return a*exp(-((x-x0)**2.)/(2.0*sigma**2.))

    def gaussian(self,Sdata): #input data for a distribution Susydat[i][1:]
        '''
        Fitting the data points to the gaussian function gaus
        Input Sdata is the distribution of the column,
        given by the suzy radar data.
        '''
        N = len(Sdata)
        x = ar(linspace(70.0,100.0,N)) #defining the height
        y = ar(Sdata) #making sure the data set is an array
        if sum(y)>=1.0:
            mean = sum(x*y)/sum(y) #finding the average value (center of the curve)
            sigma = sqrt(sum((y*(x-mean)**2.)/sum(y))) #variance for the gauss function
            try:
                popt,pcov = curve_fit(self.gaus,x,y,p0=[1,mean,sigma], maxfev=2000)
                y_fit = ar(self.gaus(x,*popt))
            except RuntimeError:
                print("Error - curve_fit failed")
                y_fit = zeros(N)
        else:
            y_fit = zeros(N)
        return x,y_fit #returns x as height and y_fit as the fitted number of occurances


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
            Sdata = Susydat[i][1:]
            x,y_fit= self.gaussian(Sdata)
            susyy[i] = x[y_fit.argmax()]

            '''
            for j in range(len(Susydat[i][1:])):
                if Susydat[i][j+1] > testx:
                    testx = Susydat[i][j+1]
                    x = j+1
                susyy[i] = x + 70  #susyy is from the height 70-100 km so need to add 69 in order to convert
            '''
        return susyx_x, susyx, susyy
