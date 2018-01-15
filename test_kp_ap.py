from numpy import *
import Middleatmos

ma = Middleatmos.Middleatmos()

#ma.read_kp_ap('Kp_2002.dat')
ma.omniread('omni2_daily_25800.lst')
