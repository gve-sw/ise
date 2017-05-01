#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

import requests, time, sys, platform, datetime
from lxml import etree
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from subprocess import call

class ISE_Print:
	#Disable warnings since we are not verifying SSL
	requests.packages.urllib3.disable_warnings()

	def chron_job(self):
		"""
			This method takes no parameters and fabricates the same functionality as a unix based
			chron job. To avoid security risks with root privelgaes, this method can be used to allow the program
			to run at only designated time intervals. This uses the datetime module and parses through the
			current system time, and checks for an equivelency at certain character postions. The position at which
			the comparison is made will determine the time interval (the lower the indexed position- the greater the
			time interval)
		"""
		while(1):
			tme = datetime.datetime.now()
			# test for equivelency can be altered to fit scheduling requirements
			# if str(tme)[17:19] == '59' and (str(tme)[20:23]) >= '999':
			if str(tme)[18] == '9' and (str(tme)[20:23]) >= '999': #causes the program to run every 10 seconds
				time.sleep(.2)
				return tme

	def wipe_guest(self, user, pwd, ip):
		"""
			***FOR TESTING AND DEVELOPMENT ENVIRONMENTS ONLY- THIS METHOD WILL WIPE ENTIRE GUEST DB***
			Used for testing in environments where guest users are generated durring testing, this method
			provides an easy way to start with a fresh DB at run time- this is useful for development environments 
			where a single user can be authenticated mutliple times without having to manually delete guest
			user information
		"""
		print "Wiping Guest Database..."
		id_list=[]
		# Quereying entire database
		url = "https://"+ip+":9060/ers/config/guestuser/"
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
		# represents the xml response as an iterable tree
		root = etree.fromstring(str(response.text))
		for count in range (0, int(root.attrib['total'])):
			id_list.append(str(root[0][count].attrib['id']))
		# querying each user by id to delete from guest DB
		for resource in id_list:
			url = "https://"+ip+":9060/ers/config/guestuser/"+resource
			headers={
				'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
				'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
			}
			requests.request("DELETE", url, auth=(user,pwd), headers=headers, verify=False)

	def get_convert_time(self, datetime):
		"""
			Converts the datetime module string into a string containing the date in the same format as ISE. 
			ISE represents date and time as 'dd-mon-yy hh.mm.ss' where mon is the three letter abbreviation for the 
			current month. Used when it is necessary to filter the queried response. It is important to not that ISE
			uses a 12 hour clock, and datetime uses a 24 hour clock-- so conversion between the two has been accounted for.
		"""
		# Dictionary containging numeric to abbreviation conversions
		abbrv = {'01':'jan', '02':'feb', '03':'mar', '04':'apr', '05':'may', '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec'}
		dash = '-'
		dot = '.'
		space = ' '
		
		# parsing through datetime string to convert and reorder values
		time_s = str(datetime)
		year = time_s[2:4]
		month = time_s[5:7]
		day = time_s[8:10]
		if int(time_s[11:13]) == 12:
			hh = str(int(time_s[11:13]))
		elif (int(time_s[11:13]))%12 < 10:
			hh = '0'+str((int(time_s[11:13]))%12)
		else:
			hh = str((int(time_s[11:13]))%12)
		mm = time_s[14:16]
		ss = time_s[17:19]
		new_time= day+dash+abbrv[month]+dash+year+space+hh+dot+mm#+dot+ss

		return new_time

	def recent_guests(self, user, pwd, ip, master_list):
		"""
			Accepts standard arguments (credentials, and management IP address)- also accepts local database of 
			users that have been previously queried by the program. This master list will keep track of all users
			that have registered a device with ISE- whether they have been approved by a sponsor or not. This is to 
			ensure that only the users that have registered since the last query are identified. It does so by requesting 
			the ISE database of guest users, and filtering the response with only entries that have a status of 'PENDING_APPROVAL'
		"""
		id_list=[]
		#filter the query by the status that we are looking for
		url = "https://"+ip+":9060/ers/config/guestuser?filter=status.EQ.PENDING_APPROVAL"
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
		root = etree.fromstring(str(response.text))
		print "Number of recent : "+ str(root.attrib['total'])
		# iterating through the list of returned users
		for count in range (0, int(root.attrib['total'])):
			print str(count+1)+".\t"+"Guest: "+str(root[0][count].attrib['name'])
			print"\t"+str(root[0][count].tag)+" : "+str(root[0][count].attrib['id'])
			# checking if the user in the response has registered (is in the master list)
			if str(root[0][count].attrib['id']) not in master_list:
				#id list will hold the most recent users waiting for approval
				id_list.append(str(root[0][count].attrib['id']))
				master_list.append(str(root[0][count].attrib['id']))
		return id_list

	def get_user_name(self, user, pwd, ip, id_list):
		"""
			Retrieves all of the names of the registered guests contained in the given list. The function will return
			a subsequest list of names of guest users whose index will correspond with the entries in the list of user IDs.
			The guest names will be used when notifying the sponsor through Spark to see whether or not the user should be 
			approved.
		"""
		name_list=[]
		file = open('ise-out.txt', 'w')
		for resource in id_list:
			url = "https://"+ip+":9060/ers/config/guestuser/"+resource
			headers={
				'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
				'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
			}
			response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
			root = etree.fromstring(str(response.text))
			name = str(root[3][3].text)+' '+str(root[3][4].text+' from '+str(root[3][0].text))
			name_list.append(name)
		return name_list

	def approve_user_by_id(self, user, pwd, ip, id_list):
		"""
			Approves group of users specified by a list of users who have received sponsor approval. The given
			list will contain the unique resource id of the target user. The method will iterate through the 
			list and send a request for each individual user.
		"""
		for resource in id_list:
			url = "https://"+ip+":9060/ers/config/guestuser/approve/"+resource
			headers={
				'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
				'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
			}
			response = requests.request("PUT", url, auth=(user,pwd), headers=headers, verify=False)
			print response.text

	def guest_user_by_id(self, user, pwd, ip, id_list):
		"""
			Queries users in a list specified by the given id_list. These users have been approved
			and will now have a customizable guest badge containing relevent information. The information
			from the badge is gathered through parsing the xml [tree] returned by the request- the values below can
			be altered to obtain different badge information. Upon querying the users information, the data will then
			be written to a temporary text file which then then be used for formatting the badge. 
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
			print response.text
			root = etree.fromstring(str(response.text))
			print "\n\nResponse:\n"
			file.write(''+str(root[3][3].tag)+' : '+str(root[3][3].text)+'\n')
			file.write(''+str(root[3][4].tag)+' : '+str(root[3][4].text)+'\n')
			file.write(''+str(root[3][0].tag)+' : '+str(root[3][0].text)+'\n')
			file.write(''+str(root[3][1].tag)+' : '+str(root[3][1].text)+'\n')
			file.write('\n')
		file.close()

	def all_guest_users(self, user, pwd, ip):
		"""
			Queries all guests (both pending and approved) saved in the ISE database. Prints all of the
			users returned by the query
		"""
		url = "https://"+ip+":9060/ers/config/guestuser/"
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': 'application/vnd.com.cisco.ise.identity.guestuser.2.0+xml'
		}
		response = requests.request("GET", url, auth=(user,pwd), headers=headers, verify=False)
		root = etree.fromstring(str(response.text))
		print "\n\nResponse:\n"
		print etree.tostring(root, pretty_print=True)

	def new_guest(self, user, pwd, ip):
		"""
			Generates a new APPROVED user based on the information defined in post-ise.xml.
			Convenient method for testing the functionality of the application when physical infrastucture
			is unavailable. Due to the administrative privelage- created users will be auto approved. Pending
			users cannot be created via the Guest API.
		"""
		url = "https://"+ip+":9060/ers/config/guestuser"
		headers={
			'Accept': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
			'Content-Type': "application/vnd.com.cisco.ise.identity.guestuser.2.0+xml",
		}

		body=''
		file = open('post-ise.xml', 'r')
		for line in file.readlines():
			body+=str(line)
		file.close
		response = requests.request("POST", url, auth=(user,pwd), headers=headers, data=body, verify=False)
		print response.text

	def get_OS(self):
		"""
			For compatibility purposes, the application can only perform print operations on UNIX based systems.
			This includes Mac and Linux (and Linux derivatives). Other functionality other than printing can still be
			utilized, yet the printing daemon used will only communicate with UNIX. This method can be used to test for
			that compatibility at run time, as it returns the current platform detected by the program.
		"""
		os_plat = platform.system()
		return os_plat.lower()

	def gen_PDF(self):
		"""
			While the method accepts no parameters- it depends on the file structure where ise-out.txt exists in the current 
			working directory at runtime. Modifications can be made to detect the working directory and base the file path off
			of that, or to establish a static filepath to the desired txt file. This method will extract the raw text from the
			txt file and then format a printable PDF that can be sent to a network printer.
		"""
		pdf = canvas.Canvas("printer_output.pdf", pagesize=letter)
		pdf.drawString(72, 720, time.ctime(time.time()))
		y=648 #36
		file = open('ise-out.txt', 'r')
		for line in file.readlines():
			if line != '\n':
				line = str(line).replace('\n','')
				pdf.drawString(72, y, str(line))
			#print line
			y-=18
		file.close
		pdf.save()


	def print_PDF(self, printer_ip, os_plat):
		"""
			This method relies on the file structure that the PDF file printer_output.pdf exists in the current 
			working directory at runtime. Modifications can be made to detect the working directory and base the file path off
			of that, or to establish a static filepath to the desired PDF. If a valid OS platform is detected, the method will initialize
			the given network printer using the Line Printer Daemon, and send the desired PDF to be printed. The call() functionality is used
			to execute shell commands within the application
		"""
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
			#sys.exit(0)
