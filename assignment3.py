#!/usr/bin/python2.7
from argparse import ArgumentParser
from csv import reader
from collections import defaultdict
from operator import itemgetter
from re import search
from sys import exit
from urllib2 import URLError, urlopen

# Returns a truthy value if the URL represents an image.
def isImage(url):
    return search("\.(jpg|gif|png)$", url)
    
# Gets the type of browser the agent represents.
def getBrowser(agent):
    return search("Firefox|Chrome|Internet Explorer|Safari", agent).group(0)

# Creates a CSV reader for the data at the given URL.
def downloadData(url):
    return reader(urlopen(url))
    
if __name__ == "__main__":
    # Parse the --url argument.
    parser = ArgumentParser()
    parser.add_argument("--url", required=True)
    url = parser.parse_args().url

    # Read in the data from the URL.
    try:
        csvData = downloadData(url)
    except URLError:
        print "Could not fetch data from the given URL:", url
        exit()
    except ValueError:
        print "Invalid URL given:", url
        exit()
        
        
    # The running counts of the various statistics.
    image_rows = 0.0
    browsers = defaultdict(int)
        
    # Process the data row-by-row.
    for index, row in enumerate(csvData):
        if isImage(row[0]):
            image_rows += 1
        try:
            browsers[getBrowser(row[2])] += 1
        except:
            pass
 
    # Calculate and output results.
    percent_images = "{:.1%}".format(image_rows / (index + 1))
    max_browser = max(browsers.iteritems(), key=itemgetter(1))[0]
    print "Image requests account for", percent_images, "of all requests"
    print "The most popular browser was", max_browser
    