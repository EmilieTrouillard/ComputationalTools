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
matches = re.finditer(WIKILINK_REGEX, jsonPage['text']['*'], re.IGNORECASE | re.UNICODE)

for matchNum, match in enumerate(matches):
    print(match)
    matchNum = matchNum + 1
        
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
            
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
