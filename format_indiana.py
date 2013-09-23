#! /usr/bin/env python
import os
import csv

"""
formats the Indiana csv file for upload
"""

with open('../databases/indiana.csv', 'rbU') as csv_input:
	with open('../ready_to_upload/indiana.csv', 'wb') as csv_output:
		csvreader = csv.reader(csv_input)
		cvswriter = csv.writer(csv_output)
		for row in csvreader:
			# we have:
			# Aspleniaceae,Asplenium bradleyi,BRADLEY'S SPLEENWORT,10,
			# we want: 
			# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
				
			conservatism = row[3]
			if conservatism == '':
				native = 'non-native'
				conservatism = '0'
			else:
				native = 'native'
				
			
			common_names = row[2].replace("'", '')
			
			# write cvs row
			# Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
			if row[1].find("- see ") == -1:
				cvswriter.writerow([row[1], row[0],'', native, conservatism,'','','', common_names])
