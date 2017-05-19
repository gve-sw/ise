#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import time, datetime, sys


def chron_job():
	"""When called will return the datetime every ten minutes, exactly at hh:mm:59.999"""

	while(1):
		tme = datetime.datetime.now()#get the time now
		if str(tme)[17:19] == '59' and (str(tme)[20:23]) >= '999':
			time.sleep(.2)#sleep to avoid overwriting
			return tme


#runtime testing --> only if we call the script directly
if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	while(1):
		try:
			print chron_job() #print the time when we get a "hit" from chron_job

		except KeyboardInterrupt: #end on CTRL+C
			print
			print '\n\n\n********************************'
			print '***\t\t\t     ***\n***      Session Closed      ***'
			print '***\t\t\t     ***'
			print '********************************\n\n'
			sys.exit()
