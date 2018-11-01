# coding=utf8
import json
import re
'''
GOAL: Get all links to other wikipedia pages from the json file of a single page.
'''

# WIKILINK_REGEX = r"/<a\s+(?:[^>]*?\s+)?href=\\([\"'])\/wiki\/(.*?)\\\1/"
WIKILINK_REGEX = r'href=[\'"]?\/wiki\/([^\'" >]+)'
exFileName = 'rogerFederer.json'


with open(exFileName) as f:
    jsonPage = json.load(f)

jsonPage = jsonPage['parse']
rgx = re.compile(WIKILINK_REGEX)
matches = rgx.findall(jsonPage['text']['*'])
#matches = re.finditer(WIKILINK_REGEX, jsonPage['text']['*'], re.IGNORECASE | re.UNICODE)
matches = [match for match in matches if match[:5] != 'File:']

   
L = list(set(matches))

print(L[:20])