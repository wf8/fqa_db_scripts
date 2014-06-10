#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv

"""
formats the 20140604_WI NCNE_Final csv file for upload
"""

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

with open('../databases/20140604_WI NCNE_Final.csv', 'rbU') as csv_input:
    with open('../ready_to_upload/20140604_WI_NCNE_Final.csv', 'wb') as csv_output:
        csvreader = csv.reader(csv_input)
        cvswriter = csv.writer(csv_output)
        for row in csvreader:
            # skip header rows and any row without c of c
            if row[0] != '' and 'TBD' not in row[6]:

                # we have:
                # ABIBAL,Pinaceae,Abies balsamea; Pinus balsamea,balsam fir,FACW,-1,5, ,,ABBA,Perennial,Tree,Native,Abies balsamea (L.) Mill.,,,,,,,,,,,,,,,,,,,,,,,
                # ABUTHE,Malvaceae,ABUTILON THEOPHRASTI; ABUTILON ABUTILON,velvet-leaf,FACU,1,0, ,Introduced - naturalized,ABTH,Annual,Forb,Introduced,Abutilon theophrasti Medik.,,,,,,,,,,,,,,,,,,,,,,,
                # ACAGRA,Euphorbiaceae,ACALYPHA GRACILENS,short-stalk copper-leaf,FACU,1,0, ,Introduced - adventive,ACGR2,Annual,Forb,Introduced,Acalypha gracilens A.Gray,,,,,,,,,,,,,,,,,,,,,,,
                
                # we want: 
                # Abies amabilis,Pinaceae,ABAM,native,5,1,tree,perennial,Pacific silver fir; red fir; silver fir; lovely fir
                

                acronym = removeNonAscii(row[0])

                scientific_name = row[2].lower()
                scientific_name = removeNonAscii(scientific_name)

                common_names = row[3].lower().replace("'", '')
                common_names = removeNonAscii(common_names)

                # determine physiognomy
                # valid values: "fern", "forb", "grass", "rush", "sedge", "shrub", "tree", "vine", or "bryophyte"
                # treat all graminoids as grass
                physiognomy = removeNonAscii(row[11].lower())
                if 'juncaceae' in row[1].lower():
                    physiognomy = 'rush'                    
                if 'tree' in physiognomy:
                    physiognomy = 'tree'
                if 'shrub' in physiognomy:
                    physiognomy = 'shrub'
                if 'vine' in physiognomy:
                    physiognomy = 'vine'
                if 'forb' in physiognomy:
                    physiognomy = 'forb'
                if 'fern ally' in physiognomy:
                    physiognomy = 'bryophyte'
                if 'fern' in physiognomy:
                    physiognomy = 'fern'
                if 'grass' in physiognomy:
                    physiognomy = 'grass'

                family = removeNonAscii(row[1].lower())

                # determine wetness
                wetness = removeNonAscii(row[5])            
                if 'NA' in wetness:
                    wetness = ''
                wetness = wetness.replace('[','')
                wetness = wetness.replace(']','')

                # determine duration
                duration = removeNonAscii(row[10].lower())
                if '-' in duration:
                    duration = duration[:duration.index('-')]

                # determine nativity
                if 'native' in row[12].lower():
                    native = 'native'
                else:
                    native = 'non-native'
                
                # write cvs row
                cvswriter.writerow([scientific_name, family, acronym, native, removeNonAscii(row[6]), wetness, physiognomy, duration, common_names])
