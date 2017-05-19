#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import datetime, sys


def get_convert_time(datetime):
	"""
		Unix machines will print datetime strings in the following format: yyyy-mm-dd hh:mm:ss
		ISE represents time strings as dd-[mon]-yy hh.mm.ss where [mon] is a three letter abbreviation for month
		This converts unix time representation to ISE's representation of time
	"""

	#dictionary for converting month mm --> [mon]
	abbrv = {'01':'jan', '02':'feb', '03':'mar', '04':'apr', '05':'may', '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec'}
	#neccessary ASCII characters
	dash = '-'
	dot = '.'
	space = ' '
	
	time_s = str(datetime)
	year = time_s[2:4]
	month = time_s[5:7]
	day = time_s[8:10]
	if int(time_s[11:13]) == 12:
		hh = str(int(time_s[11:13]))
	elif (int(time_s[11:13]))%12 < 10:
		hh = '0'+str((int(time_s[11:13]))%12)
	else:
		hh = str((int(time_s[11:13]))%12)
	mm = time_s[14:16]
	ss = time_s[17:19]
	new_time= day+dash+abbrv[month]+dash+year+space+hh+dot+mm+dot+ss

	return new_time

#runtime testing --> only if we call the script directly
if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	try:
		print "Datetime now: "+str(datetime.datetime.now())
		print "Convert time: "+str(get_convert_time(datetime.datetime.now()))
		print  
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
