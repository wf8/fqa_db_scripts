#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv

"""
formats the Flora_of_Delaware_10-8-2013.csv file for upload
"""

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

with open('../databases/Flora_of_Delaware_10-8-2013.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/delaware.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if 'SCIENTIFIC NAME' not in row[0] and row[0] != '':
				# we have
				# SCIENTIFIC NAME,SCIENTIFIC NAME WITH AUTHOR,SYNONYM,SYNONYM WITH AUTHOR,COMMON NAME,FAMILY SCIENTIFIC NAME,LIFE FORM,DURATION,NATIVE,COEFFICIENT OF CONSERVATISIM RANKS,WETLAND INDICATOR STATUS,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
				# Abutilon theophrasti,Abutilon theophrasti Medik.,,,velvet-leaf,Malvaceae,Herb,Annual,,0,UPL,,

				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
				# combine the synonyms
				scientific_name = row[0].lower()
				if row[2].strip() != "":
					scientific_name = scientific_name + '; ' + row[2].lower()
					
				common_names = row[4].lower().replace("'", '')
					
				common_names = removeNonAscii(common_names)

				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[6].lower().strip()
				if 'juncaceae' in row[5].lower():
					physiognomy = 'rush'					
				elif 'tree' in physiognomy:
					physiognomy = 'tree'
				elif 'shrub' in physiognomy:
					physiognomy = 'shrub'
				elif 'vine' in physiognomy:
					physiognomy = 'vine'
				elif 'fern' in physiognomy:
					physiognomy = 'fern'
				elif 'forb' in physiognomy:
					physiognomy = 'forb'
				elif 'grass' in physiognomy:
					physiognomy = 'grass'
				elif 'sedge' in physiognomy:
					physiognomy = 'sedge'
				else:
					physiognomy = 'forb'
				
				# determine wetness
				wetness_status = { 'OBL': -5,
								   'FACW+': -4,
								   'FACW': -3,
								   'FACW-': -2,
								   'FAC+': -1,
								   'FAC': 0,
								   'FAC-': 1,
								   'FACU+': 2,
								   'FACU': 3,
								   'FACU-': 4,
								   'UPL': 5,
								 }
				if row[10] == "NI":
				    wetness = ''
				else:
				    wetness = wetness_status.get(row[10], 0)			
				
				# determine duration
				duration = row[7].lower()
					
				# determine nativity
				if 'x' in row[8].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				cvswriter.writerow([scientific_name, row[5].lower(), '', native, row[9], wetness, physiognomy, duration, common_names])
