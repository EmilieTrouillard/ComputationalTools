#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:21:47 2018

CREATES JSONNAMES.txt file to say to the preprocessor what files to consider
"""

file = open('jsonNames.txt', 'w') 
 
for i in range(175978):
    file.write(str(i) + '_wiki_part.json\n')

 
file.close() 

    
