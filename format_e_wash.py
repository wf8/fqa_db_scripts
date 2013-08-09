#! /usr/bin/env python
import os
import csv

"""
format the eastern washington mountains csv file for upload
"""

with open('../databases/eastern_washington_mountains.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/eastern_washington_mountains.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row or rows with no conservatism coefficient
			if row[0] != 'Coefficient of Conservatism' and row[0] != 'no value' and row[0] != '':
				# we have: 5,Abies amabilis,Abies amabilis,Abies amabilis,Tree,Pinaceae,native,Perennial,FACU
				# we want: Abies amabilis,Pinaceae,,native,5,1,tree,perennial,
				
				# combine the synonyms
				scientific_name = row[1]
				if scientific_name != row[2] and row[2] != '':
					scientific_name = scientific_name + ';' + row[2]
					if row[2] != row[3] and row[3] != '':
						scientific_name = scientific_name + ';' + row[3]
				elif scientific_name != row[3] and row[3] != '':		
					scientific_name = scientific_name + ';' + row[3]
				scientific_name = scientific_name.replace('&', '')
				
				# determine wetness
				wetness = 'test'
				
				# determine physiognomy
				physiognomy = 'test'
				
				# write cvs row
				cvswriter.writerow([scientific_name, row[5], '', row[6], row[0], wetness, physiognomy, row[7].lower(),''])