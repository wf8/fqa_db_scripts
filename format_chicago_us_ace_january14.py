#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv

"""
formats the Chicago Region US ACE 2014 csv file for upload
"""

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

with open('../databases/Chicago_USACE_01.16.14.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/Chicago_USACE_01.16.14.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if 'Acronym' not in row[0] and row[0] != '':
				# 2013 version:
				# Scientific Name (NWPL/Mohlenbrock),Scientific Name Synonym    (Swink & Wilhelm),Common Name           (NWPL/Mohlenbrock),Common Name Synonym (Swink & Wilhelm),Author,Midwest Region Wetland Indicator,Coefficient of Conservatism,Wetness Coefficient,Habit,Duration  ,Nativity,Scientific Family Name,Common Family Name
				# Abelmoschus esculentus,HIBISCUS ESCULENTUS,Okra,OKRA,(L.) Moench.,UPL,0,2,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# Abutilon theophrasti,ABUTILON THEOPHRASTI,Velvetleaf,VELVETLEAF,Medik.,FACU,0,1,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# Acalypha gracilens,Acalypha gracilens,Slender Three-Seed-Mercury,SLENDER MERCURY,Gray,FACU,7,1,Forb,Annual,Native,EUPHORBIACEAE,Spurge Family


				# 2014 version:
				# Acronym,Scientific Name (NWPL/Mohlenbrock),Scientific Name Synonym    (Swink & Wilhelm),Common Name           (NWPL/Mohlenbrock),Common Name Synonym (Swink & Wilhelm),Author,Midwest Region Wetland Indicator,NC-NE Region Wetland Indicator,Coefficient of Conservatism,Wetness Coefficient,Habit,Duration  ,Nativity,Scientific Family Name,Common Family Name
				# ABEESC,Abelmoschus esculentus,HIBISCUS ESCULENTUS,Okra,OKRA,(L.) Moench.,UPL,UPL,0,2,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# HIBESC,Abelmoschus esculentus,HIBISCUS ESCULENTUS,Okra,OKRA,(L.) Moench.,UPL,UPL,0,2,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# ABUTHE,Abutilon theophrasti,ABUTILON THEOPHRASTI,Velvetleaf,VELVETLEAF,Medik.,FACU,FACU,0,1,Forb,Annual,Adventive,MALVACEAE,Mallow Family


				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
				# this script will:
				#	1) generate a new csv for the 2014 version
				# another script will then use that csv to:
				# 	1) update the existing taxa in this fqa db (adding the acronym)
				#	2) add any new taxa that weren't in the 2013 version

				acronym = removeNonAscii(row[0])

				# combine the synonyms
				scientific_name = row[1].lower()
				if scientific_name != row[2].lower():
					scientific_name = scientific_name + '; ' + row[2].lower()
					
				scientific_name = removeNonAscii(scientific_name)

				common_names = row[3].lower().replace("'", '')
				if common_names != row[4].lower().replace("'", ''):
					common_names = common_names + '; ' + row[4].lower().replace("'", '')
					
				common_names = removeNonAscii(common_names)

				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = removeNonAscii(row[10].lower())
				if 'juncaceae' in row[13].lower():
					physiognomy = 'rush'					
				
				family = removeNonAscii(row[13].lower())

				# determine wetness
				wetness = removeNonAscii(row[9])			
				
				# determine duration
				duration = removeNonAscii(row[11].lower())
					
				# determine nativity
				if 'native' in row[12].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				cvswriter.writerow([scientific_name, family, acronym, native, removeNonAscii(row[8]), wetness, physiognomy, duration, common_names])
