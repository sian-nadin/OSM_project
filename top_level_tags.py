# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
# return a dictionary with the tag name as the key and number of times
# this tag can be encountered in the map as value.
    tags = {}
    # iteratively parse the file
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags
