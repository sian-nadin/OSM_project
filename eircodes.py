import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

eircode_re = re.compile(r'[A-Za-z]\d{2}\s[A-Za-z\d]{4}')
def is_eircode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_eircode(eircodes,value):
    m = eircode_re.search(value)
    if m:
        eircode = m.group()
        eircodes[eircode].add(value)
    value = value.upper()
    eircodes[value].add(value)
    return eircodes

def audit(osmfile):
    osm_file = open(osmfile, "r")
    eircodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_eircode(tag):
                    eircodes = audit_eircode(eircodes,tag.attrib['v'])
    osm_file.close()
    return eircodes
