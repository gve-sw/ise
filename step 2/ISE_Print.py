import requests, time, sys, platform, datetime
from lxml import etree
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from subprocess import call

class ISE_Print:
	#Disable warnings since we are not verifying SSL
	requests.packages.urllib3.disable_warnings()

	def chron_job(self):
		while(1):
			tme = datetime.datetime.now()
			# if str(tme)[17:19] == '59' and (str(tme)[20:23]) >= '999':
			# 	print "hit: "+str(tme)
			# 	time.sleep(.2)
			if str(tme)[18] == '9' and (str(tme)[20:23]) >= '999':
				#print "hit [datetime]:\t"+str(tme)
				#print "hit [convtime]:\t"+str(get_convert_time(tme))
				#ret_str = str(get_convert_time(self, tme))[:15]
				time.sleep(.2)
				return tme

	def wipe_guest(self, user, pwd, ip):
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

	def get_convert_time(self, datetime):
		abbrv = {'01':'jan', '02':'feb', '03':'mar', '04':'apr', '05':'may', '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec'}
		dash = '-'
		dot = '.'
		space = ' '
		
		time_s = str(datetime)
		year = time_s[2:4]
		month = time_s[5:7]
		day = time_s[8:10]
		if int(time_s[11:13])+4 == 12:
			hh = str(int(time_s[11:13])+4)
		elif (int(time_s[11:13])+4)%12 < 10:
			hh = '0'+str((int(time_s[11:13])+4)%12)
		else:
			hh = str((int(time_s[11:13])+4)%12)
		mm = time_s[14:16]
		ss = time_s[17:19]
		new_time= day+dash+abbrv[month]+dash+year+space+hh+dot+mm#+dot+ss

		return new_time

	def recent_guests(self, user, pwd, ip, tme):
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


	def recent_approved(self, user, pwd, ip, guest_list):
		id_list=[]
		url = "https://"+ip+":9060/ers/config/guestuser?filter=status.EQ.Approved"
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
		
		temp = guest_list
		
		for guest in id_list:
			isOld = False
			for approved in guest_list:
				if guest == approved:
					isOld ==True
			if isOld == True:
				temp.remove(guest)
			else:
				temp.append(guest)

		return temp


	def recent_pending(self, user, pwd, ip, guest_list):
		id_list=[]
		url = "https://"+ip+":9060/ers/config/guestuser?filter=status.EQ.Pending"
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
		
		temp = guest_list
		
		for guest in id_list:
			isOld = False
			for pending in guest_list:
				if guest == pending:
					isOld ==True
			if isOld == True:
				temp.remove(guest)
			else:
				temp.append(guest)

		return id_list

	def guest_user_by_id(self, user, pwd, ip, id_list):
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
			print (root[3][4].tag, root[3][4].text)
			print (root[3][5].tag, root[3][5].text)
			print (root[3][0].tag, root[3][0].text)
			print '*************'
			print (root[3][1].tag, root[3][1].text)
			print '*************'
			# for child in root:
			# 	for grand in child:
			# 		print(grand.tag, grand.text)
			#print
			file.write(''+str(root[3][4].tag)+' : '+str(root[3][4].text)+'\n')
			file.write(''+str(root[3][5].tag)+' : '+str(root[3][5].text)+'\n')
			file.write(''+str(root[3][0].tag)+' : '+str(root[3][0].text)+'\n')
			file.write(''+str(root[5].tag)+' : '+str(root[5].text)+'\n')
		file.close()

	def all_guest_users(self, user, pwd, ip):
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
		os_plat = platform.system()
		return os_plat.lower()

	def gen_PDF(self):
		pdf = canvas.Canvas("printer_output.pdf", pagesize=letter)
		pdf.drawString(72, 720, time.ctime(time.time()))
		y=648 #36
		file = open('ise-out.txt', 'r')
		for line in file.readlines():
			if line != '\n':
				line = str(line).replace('\n','')
				pdf.drawString(72, y, str(line))
			#print line
			y-=36
		file.close
		pdf.save()

	def print_PDF(self, printer_ip, os_plat):
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

		# elif os_plat.lower() == 'windows':
		# 	print "Running on Windows"
		# 	print_name_arg = "-S"+printer_name
		# 	win32api.ShellExecute (["print https://64.102.40.215 filename"])
		# 	win32api.ShellExecute (["lpr", print_name_arg, "-d", filename])

		else:
			print "Incompatible OS -- application designed to work with Unix based Kernels"
			print "Exiting..."
			#sys.exit(0)
