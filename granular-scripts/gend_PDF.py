#!/usr/bin/env python
__author__ = "Michael Castellana, Chiara Pietra"
__email__ = "micastel@cisco.com"
__status__ = "Development"

#import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def gen_PDF():
	"""Generates PDF from raw test for persistent formatting when printing-- reads from predefined temp file"""
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


#runtime testing --> only if we call the script directly
if __name__ == '__main__':


	try:
		gen_PDF() 
		print '\n\n\n********************************'
		print '***\t\t\t     ***\n***      Session Closed      ***'
		print '***\t\t\t     ***'
		print '********************************\n\n'

	except: #issues
		print
		print 'Problem occurred-- exiting with System Code (1)'
		sys.exit(1)
