#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
import requests, sys
from lxml import etree


def recent_guests(user, pwd, ip, tme):
	id_list=[]
	url = "https://"+ip+":9060/ers/config/guestuser?filter=creationTime.STARTSW."+tme
	headers={
		'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
		'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
	}
	print url
	response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
	root = etree.fromstring(str(response.text))
	if int(root.attrib['total'])!= 0:
		print "Response:"
		#print etree.tostring(root, pretty_print=True)
		print '\n'
	print
	print "Number of recent : "+ str(root.attrib['total'])
	for count in range (0, int(root.attrib['total'])):
		print str(count+1)+".\t"+"Guest: "+str(root[0][count].attrib['name'])
		print"\t"+str(root[0][count].tag)+" : "+str(root[0][count].attrib['id'])
		id_list.append(str(root[0][count].attrib['id']))
	return id_list

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
	tme=" " #tme must be formatted according to ISEs dd-[mon]-yy hh.mm.ss

	#try:
	recent_guests(user, pwd, ip, tme) 
	print
	print '\n\n\n********************************'
	print '***\t\t\t     ***\n***      Session Closed      ***'
	print '***\t\t\t     ***'
	print '********************************\n\n'

	# except: #issues
	# 	print
	# 	print 'Problem occurred-- exiting with System Code (1)'
	# 	sys.exit(1)
