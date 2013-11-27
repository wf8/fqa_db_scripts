#! /usr/bin/env python
import os
import csv

"""
formats the mid Atlantic csv file for upload
"""

coefficients = [8,9,10,11,12,13]
regions = {8:'CP',9:'PD',10:'RV',11:'AP',12:'GP',13:'PI'}
for c in coefficients:
	with open('../databases/Mid-Atlantic.csv', 'rbU') as csv_input:
		with open('../ready_to_upload/Mid_Atlantic_' + regions[c] + '.csv', 'wb') as csv_output:
			csvreader = csv.reader(csv_input)
			cvswriter = csv.writer(csv_output)
			for row in csvreader:
				# skip the header row or rows with no coefficient of conservatism
				if row[0] != 'Accepted Symbol' and row[0] != '' and row[c] != '':
					# we want: Abies amabilis,Pinaceae,,native,5,1,tree,perennial,
					
					acronym = row[0]
					family = row[2]
					scientific_name = row[1].replace('.','')
					c_o_c = row[c]

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
					wetness = wetness_status.get(row[19], 0)			
					
					# determine physiognomy
					# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
					# treat all graminoids as grass
					physiognomy = row[17].lower()
					
					# determine duration
					duration = row[16]
						
					# determine nativity
					native = row[15]
					
					# write cvs row
					cvswriter.writerow([scientific_name, family, acronym, native, c_o_c, wetness, physiognomy, duration,''])
