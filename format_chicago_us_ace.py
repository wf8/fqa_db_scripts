#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv

"""
formats the Chicago Region US ACE 2013 csv file for upload
"""

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

with open('../databases/chicago_us_ace.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/chicago_us_ace.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if 'Scientific Name' not in row[0] and row[0] != '':
				# we have
				# Scientific Name (NWPL/Mohlenbrock),Scientific Name Synonym    (Swink & Wilhelm),Common Name           (NWPL/Mohlenbrock),Common Name Synonym (Swink & Wilhelm),Author,Midwest Region Wetland Indicator,Coefficient of Conservatism,Wetness Coefficient,Habit,Duration  ,Nativity,Scientific Family Name,Common Family Name
				# Abelmoschus esculentus,HIBISCUS ESCULENTUS,Okra,OKRA,(L.) Moench.,UPL,0,2,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# Abutilon theophrasti,ABUTILON THEOPHRASTI,Velvetleaf,VELVETLEAF,Medik.,FACU,0,1,Forb,Annual,Adventive,MALVACEAE,Mallow Family
				# Acalypha gracilens,Acalypha gracilens,Slender Three-Seed-Mercury,SLENDER MERCURY,Gray,FACU,7,1,Forb,Annual,Native,EUPHORBIACEAE,Spurge Family

				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
				# combine the synonyms
				scientific_name = row[0].lower()
				if scientific_name != row[1].lower():
					scientific_name = scientific_name + '; ' + row[1].lower()
					
				common_names = row[2].lower().replace("'", '')
				if common_names != row[3].lower().replace("'", ''):
					common_names = common_names + '; ' + row[3].lower().replace("'", '')
					
				common_names = removeNonAscii(common_names)

				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[8].lower()
				if 'juncaceae' in row[11].lower():
					physiognomy = 'rush'					
					
				# determine wetness
				wetness = row[7]			
				
				# determine duration
				duration = row[9].lower()
					
				# determine nativity
				if 'native' in row[10].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				# write cvs row
				cvswriter.writerow([scientific_name, row[11].lower(), '', native, row[6], wetness, physiognomy, duration, common_names])