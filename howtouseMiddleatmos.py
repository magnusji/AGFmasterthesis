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

omniread_data = Matmos.omniread('omni2_daily_25800.lst') #reading Ap and F10.7 data
susyx_x, susyx,susyy, susyy_b, tempyy,tempyy_ap = \
Matmos.sort_suzy(Susydat, omniread_data) # dist data + number between 1 and 31 for height profile

seasonaldates, seasonalindices = Matmos.seasons(susyx,xx)

seasonaltemperature = tempyy[seasonalindices]
seasonaltemp_ap = tempyy_ap[seasonalindices]
Matmos.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],\
seasonaltemperature,seasonaltemp_ap,xx,yy,title='Season 2013-2014')
#mp.savefig('Figures_ap/season1314_ap.png',bbox_inches='tight')
#mp.figure()
#mp.plot(susyy[seasonalindices], seasonaltemp_ap, 'ko')

matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
print(matchDatesOH[0],matchDatesR[0])
print(matchDatesOH[1],matchDatesR[1])
print(matchDatesOH[2],matchDatesR[2])
print(matchDatesOH[3],matchDatesR[3])
print(matchDatesOH[4],matchDatesR[4])

seasonalheight = susyy[MatchR]
seasonaltempOH = yy[MatchOH]

mp.figure()
mp.plot(seasonaltempOH,seasonalheight, 'ko', label='1314')
mp.hold('on')
mp.xlabel('Temperature')
mp.ylabel('Height')
OH_data = Mread.read_oh('daily_OHtemp_1415_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH = yy[MatchOH]
mp.plot(seasonaltempOH,seasonalheight, 'ro', label='1415')
OH_data = Mread.read_oh('daily_OHtemp_1213_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH = yy[MatchOH]
mp.plot(seasonaltempOH,seasonalheight, 'go',label='1213')
OH_data = Mread.read_oh('daily_OHtemp_1112_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH = yy[MatchOH]
mp.plot(seasonaltempOH,seasonalheight, 'bo',label='1112')
OH_data = Mread.read_oh('daily_OHtemp_1011_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH = yy[MatchOH]
mp.plot(seasonaltempOH,seasonalheight, 'co',label='1011')
mp.legend(bbox_to_anchor=(0.2,0.5), loc='center left', borderaxespad=0)
mp.hold('off')
mp.savefig('Figures_ap/heightvsOHtemp.png',bbox_inches='tight')
mp.show()
