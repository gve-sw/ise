#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import requests, sys


def wipe_guest(user, pwd, ip):
	"""clears the guest database on the ise node for continuous testing purposes"""
	print "Wiping Guest Database..."
	id_list=[]
	url = "https://"+ip+":9060/ers/config/guestuser/"
	headers={
		'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
		'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
	}
	response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
	root = etree.fromstring(str(response.text))
	for count in range (0, int(root.attrib['total'])):
		id_list.append(str(root[0][count].attrib['id']))
	for resource in id_list:
		url = "https://"+ip+":9060/ers/config/guestuser/"+resource
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		requests.request("DELETE", url, auth=(user,pwd), headers=headers, verify=False)


#runtime testing --> only if we call the script directly
if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	user = 'sponsor'
	pwd  = 'Csap1'
	ip="198.18.133.27"

	#Disable warnings since we are not verifying SSL
	requests.packages.urllib3.disable_warnings()

	try:
		wipe_guest(user, pwd, ip) 
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
