#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv

"""
formats the Chicago Region US ACE 2013 csv file for upload
"""

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

with open('../databases/minnesota.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/minnesota.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if 'tsn' not in row[0] and row[0] != '':
				# we have
# tsn,C-value1,C-value2,Scientific Name,Taxon Author,Rank,Family,Genus,Common Name,MN Nativity,US Nativity,MNWI,Growth Habit,MN Listed,Duration
# 18032,4,4,Abies balsamea,(L.) P. Mill.,Species,Pinaceae,Abies,Balsam fir,Native,Native to U.S.,FACW,Tree,,Perennial
# 21674,,0,Abutilon theophrasti,Medik.,Species,Malvaceae,Abutilon,,Introduced,Introduced to U.S.,FACU-,Forb/herb,,Annual
# 28193,0,0,Acalypha rhomboidea,Raf.,Species,Euphorbiaceae,Acalypha,Three-seeded mercury,Native,Native to U.S.,FACU,Forb/herb,,Annual

				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
				scientific_name = row[3].lower()
					
				common_names = row[8].lower().replace("'", '')
				common_names = removeNonAscii(common_names)

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
				wetness = wetness_status.get(row[11].replace('[','').replace(']',''), 0)	

				family = row[6].lower()
				
				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				physiognomy = row[12].lower()
				if 'tree' in physiognomy:
					physiognomy = 'tree'
				elif 'shrub' in physiognomy:
					physiognomy = 'shrub'
				elif 'vine' in physiognomy:
					physiognomy = 'vine'
				elif 'forb' in physiognomy:
					physiognomy = 'forb'
				elif 'fern' in physiognomy:
					physiognomy = 'fern'
				elif 'graminoid' in physiognomy:
					physiognomy = 'grass'
				else:
					physiognomy = 'forb'
				if 'juncaceae' in family:
					physiognomy = 'rush'
				if 'cyperaceae' in family:
					physiognomy = 'rush'								
				
				# determine duration
				duration = row[9].lower()
				if 'perennial' in duration:
					duration = 'perennial'
				elif 'biennial' in duration:
					duration = 'biennial'
				else:
					duration = 'annual'
					
				# determine nativity
				if 'native' in row[9].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				cvswriter.writerow([scientific_name, family, '', native, row[2], wetness, physiognomy, duration, common_names])