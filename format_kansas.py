#! /usr/bin/env python
import os
import csv

"""
formats the kansas csv file for upload
"""

with open('../databases/kansas.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/kansas.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input, delimiter=',')
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row or hybrid that have no C_o_C
			if row[0] != 'Family' and row[0] != '' and row[8] != 'hybrid':
				# we have: Acanthaceae,Justicia americana,(L.) Vahl,American water-willow,P,G,0,S4,5,,,,, 
				# we want: Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
				# combine the synonyms
				scientific_name = row[1]
				family = row[0]
				common_name = row[3].replace(',', ';')
				common_name = common_name.replace("'", "")
				wetness = ""

				# determin duration
				duration = row[4].lower()
				if 'p' in duration:
					duration = 'perennial'
				elif 'a' in duration:
					duration = 'annual'
				elif 'b' in duration:
					duration = 'biennial'
				else:
					duration = 'perennial'
				
				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[5].lower()
				if 'p' in physiognomy:
					physiognomy = 'tree'
				elif 'n' in physiognomy:
					physiognomy = 'shrub'
				else:
					physiognomy = 'forb'
					
				conservatism = row[8]
				if '*' in conservatism:
					conservatism = 0
				
				# determine nativity
				if '0' in row[6]:
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				# we have: JUAM,*,JUSTICIA AMERICANA,American water-willow,P-HERB,OBL,ACANTHACEAE,G5,SNA 
				# we want: Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				cvswriter.writerow([scientific_name, family, "", native, conservatism, wetness, physiognomy, duration, common_name])
