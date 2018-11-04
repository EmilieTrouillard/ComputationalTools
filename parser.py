# coding=utf8
import json
import re
'''
GOAL: Get all links to other wikipedia pages from the json file of a single page.
'''

# DEPRECATED USED FOR PARSING JSON FROM API
# WIKILINK_REGEX = r"/<a\s+(?:[^>]*?\s+)?href=\\([\"'])\/wiki\/(.*?)\\\1/"

WIKILINK_REGEX = r'\[\[([\| \w+]*)\]\]'
rgx = re.compile(WIKILINK_REGEX)

def getLinksFromPage(page):
    '''
    For a page returns the links (Best to handle the format from here)
    '''
    return page['links']

def getTitleFromPage(page):
    '''
    For a page returns the titel (Best to handle the format from here)
    '''
    return page['title']

def parseJSON_FROMXML(fileName):
    '''
    Parses a json file generated from the xml wikipedia dump
    '''
    # REGEX
    global WIKILINK_REGEX
    rgx = re.compile(WIKILINK_REGEX)

    try :
        with open(fileName) as f:
            jsonPage = json.load(f)
    except FileNotFoundError: 
        return 'Please enter the name of an existing file'

    # Pages List
    d = []

    for page in jsonPage:
        save_page=dict()

        # Pages that are deprecated and don't contain any content.
        if 'redirect' in page.keys():
            save_page['title'] = page['redirect']['title']
            save_page['links']= []
        else:
            save_page['title'] = page['title']
            page_revision = page['revision']
            matches = rgx.findall(page_revision['text'])
            matches = [match for match in matches if match[:5] != 'File:']
            links = [onematch for match in matches for onematch in match.split('|')]
            save_page['links'] = sorted(list(set(links)))
        d.append(save_page)

    nonEmptyD = list(filter(lambda page: len(page['links']) > 0, d))

    return nonEmptyD

# TESTABLE 
if __name__ == '__main__':
    print('Enter the input file:')
    jsonFile = input()
    print(parseJSON_FROMXML(jsonFile))

