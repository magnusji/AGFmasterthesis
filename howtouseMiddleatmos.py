from numpy import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as mp
import datetime
#import Read_four_lines as Rf # Now included in the Middleatmos class.
import Middleatmos
import scipy.stats as stats
from scipy import exp, asarray as ar

Matmos = Middleatmos.Middleatmos()
Mread = Middleatmos.Read_four_lines()

OH_data = Mread.read_oh('daily_OHtemp_1314_mies.dat')
Susydat = Mread.read_suzy('distribution_ht.txt')
xx,yy = Mread.sort_oh(OH_data)

omniread_data = Matmos.omniread('omni2_daily_25800.lst')
susyx_x, susyx,susyy, susyy_b, tempyy,tempyy_ap = Matmos.sort_suzy(Susydat, omniread_data) # dist data + number between 1 and 31 for height profile

seasonaldates, seasonalindices = Matmos.seasons(susyx,xx)

seasonaltemperature = tempyy[seasonalindices]
seasonaltemp_ap = tempyy_ap[seasonalindices]
Matmos.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],seasonaltemperature,seasonaltemp_ap,xx,yy)
#mp.savefig('Figures/season1314_ap.png',bbox_inches='tight')
#mp.figure()
#mp.plot(susyy[seasonalindices], seasonaltemp_ap, 'ko')
mp.show()
