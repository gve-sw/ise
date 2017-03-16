#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import requests, sys
from lxml import etree


def all_guest_users(user, pwd, ip):
	""" Queries all registered Guests"""
		url = "https://"+ip+":9060/ers/config/guestuser/"
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
		root = etree.fromstring(str(response.text))
		print "\n\nResponse:\n"
		print etree.tostring(root, pretty_print=True)

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

	try:
		all_guest_users(user, pwd, ip) 
		print
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
