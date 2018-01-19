# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            continue
    return users


def number_of_users(OSMFILE):
    users = process_map(OSMFILE)
    print('Number of unique contributors:', len(users))
