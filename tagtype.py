import xml.etree.cElementTree as ET
import re


#Regex patterns
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# check the "k" value for each "<tag>"
def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            if lower.search(tag.attrib['k']):
                keys['lower'] += 1
            elif lower_colon.search(tag.attrib['k']):
                keys['lower_colon'] += 1
            elif problemchars.search(tag.attrib['k']):
                print(tag.attrib)
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0,
            "lower_colon": 0,
            "problemchars": 0,
            "other": 0}
    for _, element in ET.iterparse(filename):
      keys = key_type(element, keys)

    return keys
