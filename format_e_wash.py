#! /usr/bin/env python
import os
import csv

"""
format the eastern washington mountains csv file for upload
"""

with open('../databases/eastern_washington_mountains.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in csvreader:
		print ', '.join(row)