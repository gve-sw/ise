#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import requests, sys
from lxml import etree


def guest_user_by_id(user, pwd, ip, id_list):
	"""
		Takes a list of resource ids and iterates through that list
		Each iteration it calls for the Guest user by ID and then outputs the
		relevent information to a temporary ise-out.txt file
	"""
	info_list=[]
	file = open('ise-out.txt', 'w')
	for resource in id_list:
		url = "https://"+ip+":9060/ers/config/guestuser/"+resource
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
		root = etree.fromstring(str(response.text))
		print "\n\nResponse:\n"
		print etree.tostring(root, pretty_print=True)
		print
		print (root[3][3].tag, root[3][3].text)
		print (root[3][4].tag, root[3][4].text)
		print (root[3][0].tag, root[3][0].text)
		print (root[3][1].tag, root[3][1].text)


		#writing the guest info to file
		# file.write(''+str(root[3][4].tag)+' : '+str(root[3][4].text)+'\n')
		# file.write(''+str(root[3][5].tag)+' : '+str(root[3][5].text)+'\n')
		# file.write(''+str(root[3][0].tag)+' : '+str(root[3][0].text)+'\n')
		# file.write(''+str(root[5].tag)+' : '+str(root[5].text)+'\n')
	file.close()

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
	id_list=["cc916e40-2f58-11e7-a005-005056ad1b3a"] #this list will be populated programmatically at runtime when in production

	try:
		guest_user_by_id(user, pwd, ip, id_list) 
		print
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
