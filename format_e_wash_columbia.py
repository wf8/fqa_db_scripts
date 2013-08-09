#! /usr/bin/env python
import os
import csv

"""
formats the eastern Washington Columbia Basin csv file for upload
"""

with open('../databases/eastern_washington_columbia_basin.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/eastern_washington_columbia_basin.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row or rows with no conservatism coefficient
			if row[0] != 'Coefficient of Conservatism' and row[0] != 'no value' and row[0] != '':
				# we have: 5,Abies amabilis,Abies amabilis,Abies amabilis,Tree,Pinaceae,Native,N,Perennial,Tolerant,Slow,FACU,Tree
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
				# -5 = Obligate Wetland = OBL
				# -4 = Facultative Wetland+ = FACW+
				# -3 = Facultative Wetland = FACW
				# -2 = Facultative Wetland- = FACW-
				# -1 = Facultative+ = FAC+
				# 0 = Facultative = FAC
				# 1 = Facultative- = FAC-
				# 2 = Facultative Upland+ = FACU+
				# 3 = Facultative Upland = FACU
				# 4 = Facultative Upland- = FACU-
				# 5 = Upland = UPL
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
				wetness = wetness_status.get(row[11], 0)			
				
				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[4].lower()
				if 'tree' in physiognomy:
					physiognomy = 'tree'
				elif 'shrub' in physiognomy:
					physiognomy = 'shrub'
				elif 'vine' in physiognomy:
					physiognomy = 'vine'
				elif 'fern' in physiognomy:
					physiognomy = 'fern'
				elif 'forb' in physiognomy:
					physiognomy = 'forb'
				elif 'graminoid' in physiognomy:
					physiognomy = 'grass'
				else:
					physiognomy = 'forb'
					
				if 'Cyperaceae' in row[5]:
					physiognomy = 'sedge'
				if 'Juncaceae' in row[5]:
					physiognomy = 'rush'
				
				# determine duration
				if 'perennial' in row[8].lower():
					duration = 'perennial'
				elif 'annual' in row[8].lower():
					duration = 'annual'
				elif 'biennial' in row[8].lower():
					duration = 'biennial'
					
				# determine nativity
				if 'native' in row[6].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				cvswriter.writerow([scientific_name, row[5], '', native, row[0], wetness, physiognomy, duration,''])