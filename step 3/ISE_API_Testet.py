#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com, cpietra@cisco.com"
__status__ = "Development"

"""
WARNING:
This script is meant for educational purposes only.
Any use of these scripts and tools is at
our own risk. There is no guarantee that
they have been through thorough testing in a
comparable environment and we are not
responsible for any damage or data loss
incurred with their use.

INFORMATION:
If you have further questions about this API and script, please contact GVE. Here are the contact details:
   For internal Cisco employees, please contact GVE at http://go2.cisco.com/gve
   For Cisco partners, please open a case at www.cisco.com/go/ph
"""


import ISE_Print
import sys, thread, time
import ISE_Spark

if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	#Authentication Information
	sponsor_user = 'sponsor'
	pwd  = 'Csap1'
	ip="198.18.133.27"
	printer_ip = "64.102.40.215"

	#default placeholder
	tme = ''
	room = ''
	approved_list = []
	pending_list = []
	masterList = []

	roomName = 'ISE-Test-1'
	#toggle and define room id below to utilize pre-existing room containg ISE bot
	roomID = ISE_Spark.ISE_Spark().create_room(roomName)
	# print roomID
	#roomID = "Y2lzY29zcGFyazovL3VzL1JPT00vM2E2Y2NiMjAtMmY1YS0xMWU3LTg0MjItZWY0MTU3ZjQyOGFi"

	if roomID:
		#populated the room with desired admins
		email = ['cpietra@cisco.com','micastel@cisco.com']
		for item in email:
		    user = ISE_Spark.ISE_Spark().add_user(roomID, item)   #add_user() can be True or False
	    

	itr = 1
	#determines OS platform
	print "OS Platform Detected: "+ISE_Print.ISE_Print().get_OS()
	print
	#qerying all current guests at run time
	print "All Current Guests Registered: "
	ISE_Print.ISE_Print().all_guest_users(sponsor_user, pwd, ip)
	
	
	while(1):
		try:
			print "Iteration: "+str(itr) #prints the current iteration of the application

			chron = ISE_Print.ISE_Print().chron_job() #determines the scheduling for the application
			tme = ISE_Print.ISE_Print().get_convert_time(chron) #converts date time to time recognized by ISE


			pending_list = ISE_Print.ISE_Print().recent_guests(sponsor_user, pwd, ip, masterList) #query all pending users
			names = ISE_Print.ISE_Print().get_user_name(sponsor_user, pwd, ip, pending_list) #get the names of the users to send into spark
			

			ISE_Spark.ISE_Spark().approve_pending(roomID, pending_list, names, approved_list) #send pending users to sponsor via spark for authentication


			ISE_Print.ISE_Print().approve_user_by_id(sponsor_user, pwd, ip, approved_list) #approve all users designated for approval according to sponsor			

			#print all new approved users
			if len(approved_list) > 0:
				ISE_Print.ISE_Print().guest_user_by_id(sponsor_user, pwd, ip, approved_list)
				ISE_Print.ISE_Print().gen_PDF()
				ISE_Print.ISE_Print().print_PDF(printer_ip, ISE_Print.ISE_Print().get_OS())


			approved_list = [] #flush the queue
			itr+=1 #keep track of iterations


		#provide user with gracefull exit to end the process and all threads with ^C (CTRL+C)
		except KeyboardInterrupt:
			print
			#ISE_Print.ISE_Print().wipe_guest(user, pwd, ip)
			print '\n\n\n********************************'
			print '***\t\t\t     ***\n***      Session Closed      ***'
			print '***\t\t\t     ***'
			print '********************************\n\n'
			sys.exit()
