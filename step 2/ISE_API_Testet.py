import ISE_Print
import sys

if __name__ == '__main__':
	print '\n\n\n========================================'
	print '|+++\t\t\t            +++|\n|+++      ISE SOFTWARE PROJECT      +++|'
	print '|+++\t\t\t            +++|'
	print '========================================\n\n'

	user = 'sponsor'
	pwd  = 'Csap1'
	ip="198.18.133.27"
	printer_ip = "64.102.40.215"


	itr = 1
	print "OS Platform Detected: "+ISE_Print.ISE_Print().get_OS()
	print
	print "All Current Guests Registered: "
	ISE_Print.ISE_Print().all_guest_users(user, pwd, ip)
	
	
	while(1):
		try:
			print "Iteration: "+str(itr)
			chron = ISE_Print.ISE_Print().chron_job()
			tme = ISE_Print.ISE_Print().get_convert_time(chron)
			res_list = ISE_Print.ISE_Print().recent_guests(user, pwd, ip, tme)
			if len(res_list) > 0:
				ISE_Print.ISE_Print().guest_user_by_id(user, pwd, ip, res_list)
				ISE_Print.ISE_Print().gen_PDF()
				ISE_Print.ISE_Print().print_PDF(printer_ip, ISE_Print.ISE_Print().get_OS())
			print "\n\n\n"
			itr+=1

		except KeyboardInterrupt:
			print
			ISE_Print.ISE_Print().wipe_guest(user, pwd, ip)
			print '\n\n\n********************************'
			print '***\t\t\t     ***\n***      Session Closed      ***'
			print '***\t\t\t     ***'
			print '********************************\n\n'
			sys.exit()

