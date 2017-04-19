import ISE_Print
import sys, thread, time
import ISE_Spark

if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	sponsor_user = 'sponsor'
	pwd  = 'Csap1'
	ip="198.18.133.27"
	printer_ip = "64.102.40.215"

	tme = ''

	room = ''
	approved_list = []
	pending_list = []
	masterList = []

	roomName = 'ISE-Test-1'
	roomID = ISE_Spark.ISE_Spark().create_room(roomName)
	#roomID = "Y2lzY29zcGFyazovL3VzL1JPT00vYzYxODI2ODAtMjUxMi0xMWU3LTg3NjktMmJhNThlZmUyMTNh"

	if roomID:
    # email = 'cpietra@cisco.com'
	    email = 'micastel@cisco.com'
	    user = ISE_Spark.ISE_Spark().add_user(roomID, email)   #add_user() can be True or False
	    



	itr = 1
	print "OS Platform Detected: "+ISE_Print.ISE_Print().get_OS()
	print
	print "All Current Guests Registered: "
	ISE_Print.ISE_Print().all_guest_users(sponsor_user, pwd, ip)
	
	
	while(1):
		try:
			print "Iteration: "+str(itr)
			chron = ISE_Print.ISE_Print().chron_job()
			tme = ISE_Print.ISE_Print().get_convert_time(chron)
			pending_list = ISE_Print.ISE_Print().recent_guests(sponsor_user, pwd, ip, masterList)
			names = ISE_Print.ISE_Print().get_user_name(sponsor_user, pwd, ip, pending_list)
			print names
			print "pending list"
			print pending_list
			print "master"
			print masterList
			

			print 'before: '
			print approved_list
			
			ISE_Spark.ISE_Spark().approve_pending(roomID, pending_list, names, approved_list)

			print "After: "
			print approved_list

			ISE_Print.ISE_Print().approve_user_by_id(sponsor_user, pwd, ip, approved_list)			

			if len(approved_list) > 0:
				ISE_Print.ISE_Print().guest_user_by_id(sponsor_user, pwd, ip, approved_list)
				ISE_Print.ISE_Print().gen_PDF()
				ISE_Print.ISE_Print().print_PDF(printer_ip, ISE_Print.ISE_Print().get_OS())

			approved_list = []

			
			itr+=1


		except KeyboardInterrupt:
			print
			#ISE_Print.ISE_Print().wipe_guest(user, pwd, ip)
			print '\n\n\n********************************'
			print '***\t\t\t     ***\n***      Session Closed      ***'
			print '***\t\t\t     ***'
			print '********************************\n\n'
			sys.exit()
