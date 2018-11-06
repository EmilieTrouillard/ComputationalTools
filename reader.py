'''
File that reads a set of wikipedia articles,
use the parsing tool on each,
and stores the links between pages in a serialized file.
'''
import pickle
from parser import parseJSON_FROMXML, getTitleFromPage, getLinksFromPage



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
    

