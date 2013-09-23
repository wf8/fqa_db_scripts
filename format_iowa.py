#! /usr/bin/env python
import os
import csv

"""
formats the Iowa csv file for upload
"""

with open('../databases/iowa.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/iowa.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			
			# we have:
			# ABIBAL,9,Abies balsamea,Balsam fir,TREE,-3,FACW,PINACEAE
			# ABUTHE,*,ABUTILON THEOPHRASTI,Buttonweed,A-FORB,4,FACU-,MALVACEAE
			
			# we want: 
			# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
			

			wetness = row[5]			
			
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
			if conservatism == '*' or conservatism == '**':
				native = 'non-native'
				conservatism = '0'
			else:
				native = 'native'
				
			common_names = row[3].replace("'", '').replace(",",";")
			
			# write cvs row
			# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
			cvswriter.writerow([row[2], row[7], row[0], native, conservatism, wetness, physiognomy, duration, common_names])
