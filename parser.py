# coding=utf8
import json
import re
'''
GOAL: Get all links to other wikipedia pages from the json file of a single page.
'''

# WIKILINK_REGEX = r"/<a\s+(?:[^>]*?\s+)?href=\\([\"'])\/wiki\/(.*?)\\\1/"
#WIKILINK_REGEX = r'href=[\'"]?\/wiki\/([^\'" >]+)'
WIKILINK_REGEX = r'\[\[([\| \w+]*)\]\]'
rgx = re.compile(WIKILINK_REGEX)
exFileName = 'parsed/0_wiki_part.json'
#exFileName = 'AccComp.json'

with open(exFileName) as f:
    jsonPage = json.load(f)
#for key in jsonPage:
#    print(key['title'])
d = []
for page in jsonPage:
    save_page=dict()
    if 'redirect' in page.keys():
        save_page['title'] = page['redirect']['title']
        save_page['links']= []
    else:
        save_page['title'] = page['title']
        page_revision = page['revision']
        #print(jsonPage)
        matches = rgx.findall(page_revision['text'])
        #matches = re.finditer(WIKILINK_REGEX, jsonPage['text']['*'], re.IGNORECASE | re.UNICODE)
        matches = [match for match in matches if match[:5] != 'File:']
        links = [onematch for match in matches for onematch in match.split('|')]
        save_page['links'] = sorted(list(set(links)))
    d.append(save_page)       


