'''
File that reads a set of wikipedia articles,
use the parsing tool on each,
and stores the links between pages in a serialized file.
'''
import pickle
import mmh3
from parser import parseJSON_FROMXML, getTitleFromPage, getLinksFromPage

def getPageIndex(pageName):
    '''
    Creates an Index from page name, thanks to a hash function
    We need to hash on a big enough space, to avoid collisions.
    32 bits: 2••32 = 4 294 967 296 = 429 * 10 000 000 the nbr of articles,
    64 bits: 2••64 >> 10 000 000, seems safer
    '''
    return abs(mmh3.hash64(pageName)[0])

def savePagesLinks(input, output):

    pagesJSON, _ = parseJSON_FROMXML(input)

    # FORMAT FOR EACH PAGE:
    # $pageName$: set($pagesLinked$)
    pagesDictionary = {}

    # TODO with actual JSOM
    for page in pagesJSON:
        pageTitle, links = getTitleFromPage(page), getLinksFromPage(page)
        links = list(map(lambda pageLinked: getPageIndex(pageLinked), links))
        pagesDictionary[getPageIndex(pageTitle)] = links

    # Saving data in serialized file.
    outfile = open(pickledFileName,'wb')
    pickle.dump(pagesDictionary,outfile)
    outfile.close()

# TESTABLE
if __name__ == '__main__':
    print('Enter the name of the file from which you want to read the articles:')
    articlesFile = input()
    print('Enter the name of the file in which you want to store the links:')
    pickledFileName = input()
    
    savePagesLinks(articlesFile, pickledFileName)
    

