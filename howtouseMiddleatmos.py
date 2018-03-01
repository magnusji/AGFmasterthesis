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

OH_data = Mread.read_oh('daily_OHtemp_1213_mies.dat')
Susydat = Mread.read_suzy('distribution_ht.txt')
xx,yy = Mread.sort_oh(OH_data)

omniread_data = Matmos.omniread('omni2_daily_25800.lst') #reading Ap and F10.7 data
susyx_x, susyx,susyy, susyy_b, tempyy,tempyy_ap = \
Matmos.sort_suzy(Susydat, omniread_data) # dist data + number between 1 and 31 for height profile

seasonaldates, seasonalindices = Matmos.seasons(susyx,xx)

seasonaltemperature = tempyy[seasonalindices]
seasonaltemp_ap = tempyy_ap[seasonalindices]
Matmos.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],\
seasonaltemperature,seasonaltemp_ap,xx,yy,title='Season 2012-2013')
mp.savefig('Figures_ap/season1213_ap.png',bbox_inches='tight')
#mp.figure()
#mp.plot(susyy[seasonalindices], seasonaltemp_ap, 'ko')

def seasonalplots(FilenameOH, title='title', figurename='nameforsaving'):
    OH_data = Mread.read_oh(FilenameOH)
    xx,yy = Mread.sort_oh(OH_data)
    seasonaldates, seasonalindices = Matmos.seasons(susyx,xx)
    seasonaltemperature = tempyy[seasonalindices]
    seasonaltemp_ap = tempyy_ap[seasonalindices]
    Matmos.seasonsplot_temperature_ap(seasonaldates,susyy[seasonalindices],\
    seasonaltemperature,seasonaltemp_ap,xx,yy,title=title)
    mp.savefig(figurename,bbox_inches='tight')

seasonalplots('daily_OHtemp_0809_mies.dat', title='Season 2008-2009', figurename='Figures_ap/season0809_ap.png')
seasonalplots('daily_OHtemp_1011_mies.dat', title='Season 2010-2011', figurename='Figures_ap/season1011_ap.png')
seasonalplots('daily_OHtemp_1112_mies.dat', title='Season 2011-2012', figurename='Figures_ap/season1112_ap.png')
seasonalplots('daily_OHtemp_1213_mies.dat', title='Season 2012-2013', figurename='Figures_ap/season1213_ap.png')
seasonalplots('daily_OHtemp_1314_mies.dat', title='Season 2013-2014', figurename='Figures_ap/season1314_ap.png')
seasonalplots('daily_OHtemp_1415_mies.dat', title='Season 2014-2015', figurename='Figures_ap/season1415_ap.png')

'''
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
print(matchDatesOH[0],matchDatesR[0])
print(matchDatesOH[1],matchDatesR[1])
print(matchDatesOH[2],matchDatesR[2])
print(matchDatesOH[3],matchDatesR[3])
print(matchDatesOH[4],matchDatesR[4])

seasonalheight = susyy[MatchR]
seasonaltempOH1314 = yy[MatchOH]
seasonaltempR1314 = tempyy_ap[MatchR]
mp.figure()
mp.plot(seasonaltempOH1314,seasonalheight, 'ko', label='1314')
mp.hold('on')
mp.xlabel('Temperature')
mp.ylabel('Height')
OH_data = Mread.read_oh('daily_OHtemp_1415_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH1415 = yy[MatchOH]
seasonaltempR1415 = tempyy_ap[MatchR]
mp.plot(seasonaltempOH1415,seasonalheight, 'ro', label='1415')
OH_data = Mread.read_oh('daily_OHtemp_1213_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempOH1213 = yy[MatchOH]
seasonaltempR1213 = tempyy_ap[MatchR]
mp.plot(seasonaltempOH1213,seasonalheight, 'go',label='1213')
OH_data = Mread.read_oh('daily_OHtemp_1112_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempR1112 = tempyy_ap[MatchR]
seasonaltempOH1112 = yy[MatchOH]
mp.plot(seasonaltempOH1112,seasonalheight, 'bo',label='1112')
OH_data = Mread.read_oh('daily_OHtemp_1011_mies.dat')
xx,yy = Mread.sort_oh(OH_data)
matchDatesOH,MatchOH,matchDatesR, MatchR = Matmos.date_height_temperature(xx,susyx)
seasonalheight = susyy[MatchR]
seasonaltempR1011 = tempyy_ap[MatchR]
seasonaltempOH1011 = yy[MatchOH]
R1011,P1011 = stats.pearsonr(asarray(seasonaltempR1011), asarray(seasonaltempOH1011))
print(R1011, P1011)
R1112,P1112 = stats.pearsonr(asarray(seasonaltempR1112), asarray(seasonaltempOH1112))
R1213,P1213 = stats.pearsonr(asarray(seasonaltempR1213), asarray(seasonaltempOH1213))
R1314,P1314 = stats.pearsonr(asarray(seasonaltempR1314), asarray(seasonaltempOH1314))
R1415,P1415 = stats.pearsonr(asarray(seasonaltempR1415), asarray(seasonaltempOH1415))
mp.plot(seasonaltempOH1011,seasonalheight, 'co',label='1011')
mp.legend(bbox_to_anchor=(0.2,0.5), loc='center left', borderaxespad=0)
mp.hold('off')
mp.savefig('Figures_ap/heightvsOHtemp.png',bbox_inches='tight')
mp.figure()
mp.hold('on')
mp.plot(seasonaltempR1011,seasonaltempOH1011, 'co', label='1011, R=%.2f '%R1011)
mp.plot(seasonaltempR1112,seasonaltempOH1112, 'bo', label='1112, R=%.2f '%R1112)
mp.plot(seasonaltempR1213,seasonaltempOH1213, 'go', label='1213, R=%.2f'%R1213)
mp.plot(seasonaltempR1314,seasonaltempOH1314, 'ko', label='1314, R=%.2f'%R1314)
mp.plot(seasonaltempR1415,seasonaltempOH1415, 'ro', label='1415, R=%.2f'%R1415)
mp.legend()
mp.xlabel('Meteor Temperature [K]')
mp.ylabel('OH Temperature [K]')
mp.hold('off')
mp.savefig('Figures_ap/meterotempvohtemp.png',bbox_inches='tight')
'''
mp.show()
