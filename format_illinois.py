#! /usr/bin/env python
import os
import csv

"""
formats the Illinois csv file for upload
"""

with open('../databases/illinois.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/illinois.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if row[0] != 'ACRONYM' and row[0] != '':
				# we have:
				# ACRONYM,N/A,C,W ,WETNESS,PHYSIOG.,SCIENTIFIC NAME,COMMON NAME
				# ABEESC,A,*,5,UPL,Ad A-FORB,ABELMOSCHUS ESCULENTUS,OKRA
				# ABUTHE,A,*,4,FACU-,Ad A-FORB,ABUTILON THEOPHRASTI,BUTTONWEED
				# ACADEA,N,8,5,UPL,Nt A-FORB,Acalypha deamii,LARGE-SEEDED MERCURY
				# ACAGRA,N,4,5,UPL,Nt A-FORB,Acalypha gracilens,SLENDER THREE-SEEDED MERCURY
				# ACAOST,N,1,5,UPL,Nt A-FORB,Acalypha ostryaefolia,THREE-SEEDED MERCURY
				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				

				wetness = row[3]			
				
				# determin duration
				duration = row[5].lower()
				if 'p-' in duration:
					duration = 'perennial'
				elif 'a-' in duration:
					duration = 'annual'
				elif 'b-' in duration:
					duration = 'biennial'
				else:
					duration = 'perennial'
				
				# determine physiognomy
				# valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
				# treat all graminoids as grass
				physiognomy = row[5].lower()
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
				elif 'grass' in physiognomy:
					physiognomy = 'grass'
				elif 'sedge' in physiognomy:
					physiognomy = 'sedge'
				else:
					physiognomy = 'forb'
					
				conservatism = row[2]
				if conservatism == '*':
					conservatism = 0
					
				# determine nativity
				if 'n' in row[1].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				common_names = row[7].replace("'", '')
				
				# write cvs row
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				cvswriter.writerow([row[6], '', row[0], native, conservatism, wetness, physiognomy, duration, common_names])