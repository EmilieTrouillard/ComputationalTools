# coding=utf8
import json
import re
'''
GOAL: Get all links to other wikipedia pages from the json file of a single page.

USE A PREPROCESSED MAPPING BETWEEN TITLES AND IDS
'''

# DEPRECATED USED FOR PARSING JSON FROM API
# WIKILINK_REGEX = r"/<a\s+(?:[^>]*?\s+)?href=\\([\"'])\/wiki\/(.*?)\\\1/"

WIKILINK_REGEX = r'\[\[([\| \w+]*)\]\]'
rgx = re.compile(WIKILINK_REGEX)


def getPageIndex(pageName, titletoid, redirect, count):
    try:
        return titletoid[pageName]
    except KeyError:
        if count <= 5:
            try:
                return getPageIndex(redirect[pageName], titletoid, redirect,count + 1)
            except KeyError:
                if len(pageName) > 1:
                    return getPageIndex(pageName[0].upper() + pageName[1:], titletoid, redirect,count + 1)
                else:
                    return getPageIndex(pageName.title(), titletoid, redirect,count + 1)
                    

def getLinksFromPage(page):
    '''
    For a page returns the links (Best to handle the format from here)
    '''
    return page['links']

def getTitleFromPage(page):
    '''
    For a page returns the title (Best to handle the format from here)
    '''
    return page['title']

def isCleanPage(pagename):
    if 'File:' in pagename or 'Wikipedia:' in pagename:
        return False
    return True

def parseJSON_FROMXML(fileName, titletoid, redirect):
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
        print('file '+ fileName + ' not found')
        return None

    # Pages List
    pageLinks = dict()
    for page in jsonPage:
        # Pages that are deprecated and don't contain any content.
        if 'redirect' not in page.keys():
            if isCleanPage(page['title']):
                origin_id = getPageIndex(page['title'], titletoid, redirect,0)
                page_revision = page['revision']
                matches = rgx.findall(page_revision['text'])
                matches = [match for match in matches if isCleanPage(match)]
                linkTitles = [onematch for match in matches for onematch in match.split('|')]
                links = [getPageIndex(title, titletoid, redirect,0) for title in list(set(linkTitles))]
                links = list(set([i for i in links if i is not None and i != origin_id]))
                pageLinks[origin_id] = links
            
    return pageLinks

def parseTITLES_FROMXML(fileName):
    '''
    Parses a json file generated from the xml wikipedia dump
    '''
    # REGEX
    try :
        with open(fileName) as f:
            jsonPage = json.load(f)
    except FileNotFoundError: 
        print('file '+ fileName + ' not found')
        return None

    # Pages List
    pageTitles = set()
    for page in jsonPage:
        
        if 'redirect' not in page.keys():
            if isCleanPage(page['title']):
                pageTitles.add(page['title'])
            
    return pageTitles

def parseREDIRECT_FROMXML(fileName):
    '''
    Parses a json file generated from the xml wikipedia dump
    '''
    try :
        with open(fileName) as f:
            jsonPage = json.load(f)
    except FileNotFoundError: 
        print('file '+ fileName + ' not found')
        return None

    # Pages List
    pageRedirect = dict()
    for page in jsonPage:

        # Pages that are deprecated and don't contain any content.
        if 'redirect' in page.keys():
            redirect = page['redirect']['title']
            pagename = page['title']
            if isCleanPage(redirect) and isCleanPage(pagename):
                pageRedirect[pagename] = redirect
        
    return pageRedirect


# TESTABLE 
if __name__ == '__main__':
   print('Enter the input file:')
   jsonFile = input()
   print(parseJSON_FROMXML(jsonFile))

