# coding=utf8
import json
import re
import mmh3

'''
GOAL: Get all links to other wikipedia pages from the json file of a single page.
'''

# DEPRECATED USED FOR PARSING JSON FROM API
# WIKILINK_REGEX = r"/<a\s+(?:[^>]*?\s+)?href=\\([\"'])\/wiki\/(.*?)\\\1/"

WIKILINK_REGEX = r'\[\[([\| \w+]*)\]\]'
rgx = re.compile(WIKILINK_REGEX)

def getPageIndex(pageName):
    '''
    Creates an Index from page name, thanks to a hash function
    We need to hash on a big enough space, to avoid collisions.
    32 bits: 2••32 = 4 294 967 296 = 429 * 10 000 000 the nbr of articles,
    64 bits: 2••64 >> 10 000 000, seems safer
    '''
    return abs(mmh3.hash64(pageName)[0])

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
    pageLinks = dict()
    pageRedirect = dict()
    pageTitles = dict()
    for page in jsonPage:
        #save_page=dict()

        # Pages that are deprecated and don't contain any content.
        if 'redirect' in page.keys():
            pageRedirect[getPageIndex(page['title'])] = getPageIndex(page['redirect']['title'])
            #pageRedirect.append(save_page)
        else:
            page_revision = page['revision']
            matches = rgx.findall(page_revision['text'])
            matches = [match for match in matches if match[:5] != 'File:']
            links = [getPageIndex(onematch) for match in matches for onematch in match.split('|')]
            
            pageLinks[getPageIndex(page['title'])] = list(set(links))
            #pageLinks.append(save_page)
        pageTitles[getPageIndex(page['title'])] = page['title']
    return pageLinks, pageRedirect, pageTitles

# TESTABLE 
if __name__ == '__main__':
    print('Enter the input file:')
    jsonFile = input()
    print(parseJSON_FROMXML(jsonFile))

