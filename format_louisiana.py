#! /usr/bin/env python
import os
import csv

"""
formats the Louisiana csv file for upload
"""

with open('../databases/louisiana.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/louisiana.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
				
				# we have:
				# Abutilon theophrasti,Velvet Leaf,a-forb,-1,FACU-,4,I,Malvaceae,ABTH
				# Acalypha gracilens,Slender Threeseed Mercury,a-forb,3,UPL,5,N,Euphorbiaceae,ACGR2
				# Acmella oppositifolia var. repens ,Creeping Spotflower,p-forb,3,FACW,-3,N,Asteraceae,ACOPR
				
				# we want: 
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				

				wetness = row[5]			
				
				# determin duration
				duration = row[2].lower()
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
				physiognomy = row[2].lower()
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
					
				conservatism = int(row[3])
				if conservatism < 0:
					conservatism = 0
					
				# determine nativity
				if 'n' in row[6].lower():
					native = 'native'
				else:
					native = 'non-native'
				
				common_names = row[1].replace("'", '')
				
				# write cvs row
				# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				cvswriter.writerow([row[0], row[7], row[8], native, conservatism, wetness, physiognomy, duration, common_names])
