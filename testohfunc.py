from numpy import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as mp
import datetime
#import Read_four_lines as Rf
import Middleatmos
import scipy.stats as stats
from scipy import exp, asarray as ar


a = Middleatmos.Read_four_lines()
b = Middleatmos.Middleatmos()

OH_data0203 = a.read_oh('daily_OHtemp_0203_mies.dat')
OH_data0304 = a.read_oh('daily_OHtemp_0304_mies.dat')
OH_data0405 = a.read_oh('daily_OHtemp_0405_mies.dat')
OH_data0506 = a.read_oh('daily_OHtemp_0506_mies.dat')
OH_data0607 = a.read_oh('daily_OHtemp_0607_mies.dat')
OH_data0708 = a.read_oh('daily_OHtemp_0708_mies.dat')
OH_data0809 = a.read_oh('daily_OHtemp_0809_mies.dat')
OH_data0910 = a.read_oh('daily_OHtemp_0910_mies.dat')
OH_data1011 = a.read_oh('daily_OHtemp_1011_mies.dat')
OH_data1112 = a.read_oh('daily_OHtemp_1112_mies.dat')
OH_data1213 = a.read_oh('daily_OHtemp_1213_mies.dat')
OH_data1314 = a.read_oh('daily_OHtemp_1314_mies.dat')
OH_data1415 = a.read_oh('daily_OHtemp_1415_mies.dat')
OH_data1516 = a.read_oh('daily_OHtemp_1516_mies.dat')
Susydat = a.read_suzy('distribution_ht.txt')


x0203,y0203 = a.sort_oh(OH_data0203)
x0304,y0304 = a.sort_oh(OH_data0304)
x0405,y0405 = a.sort_oh(OH_data0405)
x0506,y0506 = a.sort_oh(OH_data0506)
x0607,y0607 = a.sort_oh(OH_data0607)
x0708,y0708 = a.sort_oh(OH_data0708)
x0809,y0809 = a.sort_oh(OH_data0809)
x0910,y0910 = a.sort_oh(OH_data0910)
x1011,y1011 = a.sort_oh(OH_data1011)
x1112,y1112 = a.sort_oh(OH_data1112)
x1213,y1213 = a.sort_oh(OH_data1213)
x1314,y1314 = a.sort_oh(OH_data1314)
x1415,y1415 = a.sort_oh(OH_data1415)
x1516,y1516 = a.sort_oh(OH_data1516)

omniread_data = b.omniread('omni2_daily_25800.lst')
susyx_x, susyx,susyy, susyy_b, tempyy,tempyy_ap = b.sort_suzy(Susydat, omniread_data) # dist data + number between 1 and 31 for height profile

#print(len(susyy_b))
sigma_yyb = susyy - susyy_b
'''
mp.figure()
mp.plot(susyx, susyy, 'bo', susyx, susyy_b,'r+')

mp.figure()
mp.plot(susyx, sigma_yyb, 'bo')

mp.figure()
mp.plot(susyx,tempyy, 'bo')
mp.ylabel('temperature $^o$K')
'''
'''
fig,ax1 = mp.subplots()
ax2 = ax1.twinx()
lns1 =ax1.plot(susyx,tempyy_ap,'ro', label='temperature_ap')
lns2 = ax2.plot(susyx,susyy,'bo', label='Height')
lns3 = ax1.plot(susyx,tempyy_ap,'g*',label='temperature')
ax2.set_ylim(80,100)
fig.autofmt_xdate()
#mp.savefig('Figures/season0203.png')
lns = lns1 +lns2 + lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns,labs,loc=0)
'''



'''
xx = x0304
yy = y0304
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0304.png',bbox_inches='tight')

xx = x0405
yy = y0405
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0405.png',bbox_inches='tight')


xx = x0506
yy = y0506
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0506.png',bbox_inches='tight')

xx = x0607
yy = y0607
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0607.png',bbox_inches='tight')

xx = x0708
yy = y0708
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0708.png',bbox_inches='tight')


xx = x0809
yy = y0809
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0809.png',bbox_inches='tight')

xx = x0910
yy = y0910
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season0910.png',bbox_inches='tight')

xx = x1011
yy = y1011
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season1011.png',bbox_inches='tight')

xx = x1112
yy = y1112
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season1112.png',bbox_inches='tight')

xx = x1213
yy = y1213
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
mp.savefig('season1213.png',bbox_inches='tight')
'''
xx = x1314
yy = y1314
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]
seasonaltemp_ap = tempyy_ap[seasonalindices]
b.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],seasonaltemperature,seasonaltemp_ap,xx,yy)
mp.savefig('season1314_ap.png',bbox_inches='tight')

xx = x1415
yy = y1415
seasonaldates, seasonalindices = b.seasons(susyx,xx)
print('\n', end='')
print('seasonalindices:')
print (seasonalindices)
seasonaltemperature = tempyy[seasonalindices]

#b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemperature,xx,yy)
#b.seasonsplot_temperature(seasonaldates,susyy[seasonalindices],seasonaltemp_ap,xx,yy)
#mp.savefig('season1415.png',bbox_inches='tight')
seasonaltemp_ap = tempyy_ap[seasonalindices]
b.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],seasonaltemperature,seasonaltemp_ap,xx,yy)
mp.savefig('season1415_ap.png',bbox_inches='tight')

mp.figure()
mp.plot(seasonaldates,seasonaltemperature,'bo', label='without ap')
mp.hold('on')
mp.plot(seasonaldates,seasonaltemp_ap,'ro', label='with ap&f107')
mp.title('Temperature comparison')
mp.legend()
mp.hold('off')


mp.figure()
mp.plot(susyy,tempyy,'ro')
mp.title('Height vs temperature from model')
'''
number_n = 523  #The number in line with Suzy distributions between 0 and 5313 (-1)
Sdata = Susydat[number_n][1:]
N = len(Sdata)
x = linspace(70,100,N)
x,y_fit = b.gaussian(Sdata, 1, number_n, N, x)

mp.figure()
mp.plot(Susydat[number_n][1:], x, 'bo--', label='data')
mp.plot(y_fit,x,'ro:', label='fit')
mp.xlabel('Number of occurences')
mp.ylabel('Height in km')
mp.legend()
mp.show()

'''
'''
N = len(Susydat[number_n][1:])
print Susydat[number_n][1:]
x = ar(linspace(70,100,N))
y = ar(Susydat[number_n][1:])
mean = sum(x*y)/sum(y) #finding the average value
sigma = sqrt(sum(y*(x-mean)**2/sum(y))) #weighting for the gauss function

def gaus(x,a, x0,sigma): #making a gaussian function to fit
    return a*exp(-(x-x0)**2/(2*sigma**2))

popt,pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma]) #fitting the data to the closest possible gaussian fit given by the function gaus
y_fit = ar(gaus(x,*popt)) #fitted values for nubmer of occurences
print y_fit
max_fit_x = x[y_fit.argmax()] #Finding the height of maximum occurance after gaussian fit
max_x_nofit = x[y.argmax()] #Finding the height og max occurance in raw data
mp.figure()
mp.plot(Susydat[number_n][1:], x, 'bo--',label='data, max: %i km' %max_x_nofit)
mp.plot(y_fit,x,'ro:', label='fit, max: %i km' %max_fit_x)
mp.xlabel('Number of occurences')
mp.ylabel('Height in km')
mp.legend()
#mp.show()
mp.savefig('fitting.png',bbox_inches='tight')
print 'Max number:'
print(max(gaus(x,*popt)))

print 'max height'
print max_fit_x
#z = polyfit(Susydat[number_n], x, 2)
mp.show()
'''
'''
number_n = 3
N = len(Susydat[number_n][1:])
maxwell = stats.maxwell
params = maxwell.fit(Susydat[number_n][1:])
print params
x = linspace(70,100,N)
mp.figure()
mp.hist(Susydat[number_n][1:], bins=N, normed=True)
mp.plot(x,maxwell.pdf(x,*params), lw=3)
'''
'''
seasonaldates,seasonalsuzy = a.seasons(susyx,x0203,susyy, y0203)

fig,ax1 = mp.subplots()
ax2 = ax1.twinx()
lns1 =ax1.plot(seasonaldates,seasonalsuzy,'ro', label='suzy')
lns2 = ax2.plot(x0203,y0203,'bo', label='OH')
ax1.set_ylim(70,100)
fig.autofmt_xdate()
#mp.savefig('Figures/season0203.png')
lns = lns1 +lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns,labs,loc=0)
mp.show()
'''
'''
xx = x0304
yy = y0304
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0506.png')
mp.savefig('Figures/season0304.png')

xx = x0405
yy = y0405
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0506.png')
mp.savefig('Figures/season0405.png')
xx = x0506
yy = y0506
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0506.png')
xx = x0607
yy = y0607
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0607.png')
xx = x0708
yy = y0708
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0708.png')
xx = x0809
yy = y0809
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0809.png')
xx = x0910
yy = y0910
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season0910.png')
xx = x1011
yy = y1011
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1011.png')
xx = x1112
yy = y1112
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1112.png')
xx = x1213
yy = y1213
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1213.png')
xx = x1314
yy = y1314
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1314.png')
xx = x1415
yy = y1415
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1415.png')
xx = x1516
yy = y1516
seasonaldates,seasonalsuzy = a.seasons(susyx,xx,susyy, yy)
a.seasonsplot(seasonaldates,seasonalsuzy,xx,yy)
mp.savefig('Figures/season1516.png')
mp.show()
'''
'''
x,y = a.single_dist_suzy(Susydat,5100)
print len(x), len(y)
print y
mp.plot(x,y)


#mp.figure()
#mp.plot(susyx_x,yn,'k-')

fig,ax1 = mp.subplots()
ax2 = ax1.twinx()

ax1.plot(susyx,susyy, 'r*')

ax2.plot(x0203,y0203, 'bo')
ax2.plot(x0304,y0304, 'go')
ax2.plot(x0405,y0405, 'bo')
ax2.plot(x0506,y0506, 'go')
ax2.plot(x0607,y0607, 'bo')
ax2.plot(x0708,y0708, 'go')
ax2.plot(x0809,y0809, 'bo')
ax2.plot(x0910,y0910, 'go')
ax2.plot(x1011,y1011, 'bo')
ax2.plot(x1112,y1112, 'go')
ax2.plot(x1213,y1213, 'bo')
ax2.plot(x1314,y1314, 'go')
ax1.set_ylabel('[Km] Height of maximum meteor burnout')
ax2.set_ylabel('[$^o$K] Temperature of OH-airglow')
ax1.set_xlabel('Time')
'''

mp.show()
