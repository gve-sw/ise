#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
from subprocess import call


def print_PDF(printer_ip, os_plat):
	if os_plat.lower() == 'darwin' or os_plat.lower() == 'linux':
		IPP_addr = "https://"+printer_ip
		printer_name = "ISE_SCRIPT_PRINTER"
		print_name_arg = "-P"+printer_name
		
		call(["lpadmin", "-E", "-p", printer_name, "-v", IPP_addr, "-E"])
		print "Initializing Printer..."
		time.sleep(2)
		call(["lpr", print_name_arg, 'printer_output.pdf'])
		print "Printing..."
		time.sleep(2)
		call(["lpadmin", "-x", printer_name])
		print "Tearing down connection..."
		time.sleep(2)

	else:
		print "Incompatible OS -- application designed to work with Unix based Kernels"
		print "Exiting..."


#runtime testing --> only if we call the script directly
if __name__ == '__main__':

	printer_ip = "64.102.40.215"
	kernel = 'darwin' #assuming this is running on a UNIX system
	try:
		print_PDF(printer_ip, kernel) 
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
