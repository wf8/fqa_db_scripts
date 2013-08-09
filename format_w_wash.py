#! /usr/bin/env python
import os
import csv

"""
formats the western Washington Columbia Basin csv file for upload
"""

with open('../databases/western_washington.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/wester_washington.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row or rows with no conservatism coefficient
			if row[0] != 'Coefficient of Conservatism' and row[0] != 'no value' and row[0] != '':
				# we have: 5,Abies amabilis,Abies amabilis,Abies amabilis,N,(Dougl. ex Loud.) Dougl. ex Forbes,ABAM,"Pacific silver fir, red fir, silver fir, lovely fir",Gymnosperm,Pinaceae,Tree,Perennial,Tolerant,Slow,,No,Single Stem,None,None,Low,,FACU
				# we want: Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
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
				wetness = wetness_status.get(row[21], 0)			
				
				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[10].lower()
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
				if 'perennial' in row[11].lower():
					duration = 'perennial'
				elif 'annual' in row[11].lower():
					duration = 'annual'
				elif 'biennial' in row[11].lower():
					duration = 'biennial'
					
				# determine nativity
				if 'n' in row[4].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				common_names = row[7].replace(',', ';')
				
				# write cvs row
				cvswriter.writerow([scientific_name, row[9], row[6], native, row[0], wetness, physiognomy, duration, common_names])