import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

eircode_re = re.compile(r'[A-Za-z]\d{2}\s[A-Za-z\d]{4}')
def is_eircode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_eircode_type(eircodes,value):
    eircodes[value].add(value)
    return eircodes

def audit_eircode(osmfile):
    osm_file = open(osmfile, "r")
    eircodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_eircode(tag):
                    eircodes = audit_eircode_type(eircodes,tag.attrib['v'])
    osm_file.close()
    return eircodes

mapping = { "D01X2P2": "D01 X2P2",
            "D02X285": "D02 X285",
            "D05N7F2": "D05 N7F2",
            "D08P 89W":"D08 P89W",
            "D09VY19":"D09 VY19",
            "D15KPW7":"D15 KPW7",
            "D6WXK28":"D6W XK28",
            "d09 f6x0":"D09 F6X0"
            }

def update_eircode(osmfile):
    eircodes = audit_eircode(osmfile)
    for eircode, ways in eircodes.items():
        for name in ways:
            if eircode in mapping:
                new_name = name.replace(eircode, mapping[eircode])
                print(name, "=>", new_name)
    return name
