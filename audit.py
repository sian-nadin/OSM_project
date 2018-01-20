import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "dublin_ireland.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#A list of values we would expect to see at the end of a street name
expected = ["Street", "Avenue", "Court", "Place", "Square", "Lane", "Road", "Alley", "Arcade",
            "Bridge", "Brook", "Centre", "Close", "Crescent", "Green", "Grove", "Parade", "Park", "Terrace"]

mapping = { "Aveune": "Avenue",
            "Ave": "Avenue",
            "Cente": "Centre",
            "Cres":"Crescent",
            "hall":"Hall",
            "Heichts":"Heights",
            "lane":"Lane",
            "Rd":"Road",
            "Rd.":"Road",
            "road":"Road",
            "Roafd":"Road",
            "St":"Street",
            "St.":"Street",
            "street":"Street",
            "square":"Square",
            "heights":"Heights"
            }

"""Find street names that aren't in the expected list and add to street_types dictionary
Add specific street name to the set of values for a given street_type key"""
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

"""Find out if nested tag is a street name"""
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    #pprint.pprint(dict(street_types))
    osm_file.close()
    return street_types

"""Update street name according to the mapping dictionary"""
def update_street_name(osmfile):
    streets = audit_street(osmfile)
    for street, ways in streets.items():
        for name in ways:
            if street in mapping:
                new_name = name.replace(street, mapping[street])
                print(name, "=>", new_name)
    return name
