import argparse
import codecs
import xml.etree.ElementTree as et
from codecs import open
import re
import os

def fix(filename):
    #Function ensure the parts of the file are escaped
    #In particular the ampersand in <te

    with open(filename, mode='r', encoding='utf-16-le') as f,open(filename+'.tmp', mode='w', encoding='utf-16-le') as of:
        for line in f:
            # Ensure we only replace tags within the text tags
            match = re.match('<text>.+?<\/text>', line)
            if match:
                #Replace with excaped character
                of.write(line.replace('&', '&amp;'))
            else:
                of.write(line)

    # Clean up files
    f.close()
    of.close()
    # Move the tempory file in place
    os.remove(filename)
    os.rename(filename+'.tmp', filename)

    return filename

def testparse(filename):
    tree = et.parse(filename)

if __name__ == '__main__':
    #Generate arguements to be parsed
    parser = argparse.ArgumentParser()
    parser.add_argument('XMLfilename', help='Path to XML file with which to excape the XML files with')
    args = parser.parse_args()
    #Call function with input args
    fix(args.XMLfilename)
    testparse(args.XMLfilename)
