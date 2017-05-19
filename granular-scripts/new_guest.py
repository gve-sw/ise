#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import requests, sys
from lxml import etree


def new_guest(user, pwd, ip):
	"""For testing purposes...pulls info from predefined post-ise.xml and generates new user to query later"""
	url = "https://"+ip+":9060/ers/config/guestuser"
	headers={
		'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
		'Content-Type': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
	}

	body=''
	file = open('post-ise1.xml', 'r')
	for line in file.readlines():
		body+=str(line)
	file.close
	response = requests.request("POST", url, auth=(user,pwd), headers=headers, data=body, verify=False)
	print response.text

#runtime testing --> only if we call the script directly
if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	#Disable warnings since we are not verifying SSL
	requests.packages.urllib3.disable_warnings()

	user = 'sponsor'
	pwd  = 'Csap1'
	ip="198.18.133.27"

	new_guest(user, pwd, ip) 

	# try:
	# 	new_guest(user, pwd, ip) 
	# 	print
	# 	print '\n\n\n********************************'
	# 	print '***\t\t\t     ***\n***      Session Closed      ***'
	# 	print '***\t\t\t     ***'
	# 	print '********************************\n\n'

	# except: #issues
	# 	print
	# 	print 'Problem occurred-- exiting with System Code (1)'
	# 	sys.exit(1)
