import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    result = {}

    for dir_elem in root.findall(".//dir[@name='SN']/.."):
        parent_dir_name = dir_elem.attrib['name']
        int32_values = []
        for int32_elem in dir_elem.findall(".//int32"):
            int32_value = int(int32_elem.attrib['value'])
            int32_values.append(int32_value)
        result[parent_dir_name] = int32_values

    return result
