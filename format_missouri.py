#! /usr/bin/env python
import os
import csv

"""
formats the missouri csv file for upload
"""

with open('../databases/missouri.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/missouri.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# skip the header row 
			if row[0] != '':
				# we have:
				# ABUTH,*,ABUTILON THEOPHRASTI,,Ad A-FORB,,Malvaceae,4,FACU-,Velvetleaf
				# ACAAN,10,Acacia angustissima,,Nt SHRUB,,Leguminosae,5,UPL,Prairie Acacia
				# ACADE,10,Acalypha deamii ***,,Nt A-FORB,SU,Euphorbiaceae,3,FACU,Large-Seeded Mercury
				# ACAGR,3,Acalypha gracilens,,Nt A-FORB,,Euphorbiaceae,5,UPL,Slender Mercury
				# ACAOS ,2,Acalypha ostryaefolia,,Nt A-FORB,,Euphorbiaceae,5,UPL,Three-Seeded Mercury

				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				

				wetness = row[7]	
				
				# determine nativity
				if 'Nt ' in row[4]:
					native = 'native'
				else:
					native = 'non-native'		
				
				# determin duration
				duration = row[4].lower()
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
				elif 'grass' in physiognomy:
					physiognomy = 'grass'
				elif 'sedge' in physiognomy:
					physiognomy = 'sedge'
				else:
					physiognomy = 'forb'
					
				conservatism = row[1]
				if conservatism == '*':
					conservatism = 0
				if int(conservatism) > 10:
					conservatism = 10
				
				common_names = row[9].replace("'", '')
				
				# write cvs row
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				cvswriter.writerow([row[2], '', row[0], native, conservatism, wetness, physiognomy, duration, common_names])