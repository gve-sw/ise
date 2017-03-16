#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import platform


def get_OS():
	"""
		Detects the OS to determine if we have a valid Kernel for printing-- 
		to properly print the user must be running on a Linux Kernel 
	"""
	os_plat = platform.system()
	return os_plat.lower()

#runtime testing --> only if we call the script directly
if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	print "Kernel Detected: "+str(get_OS())
	if str(get_OS()).lower() == 'darwin': print "Running on Mac OS X"
	elif str(get_OS()).lower() == 'linux':print "Running on Linux" 
	else: "Incompatible OS-- built to work on UNIX Kernels"
	print 
