import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('Etc.Commodity.img.xml')
root = tree.getroot()

# Create a new XML tree for qualifying dirs
qualifying_root = ET.Element("root")

# Iterate over all dir elements
for dir_elem in root.findall('.//dir'):
    # Check if the dir element has a child element with name "termStart"
    term_start_elem = dir_elem.find("./int32[@name='termStart']")
    if term_start_elem is not None:
        term_start_value = term_start_elem.get('value')
        # Check if termStart value starts with '202402'
        if term_start_value.startswith('202402') or term_start_value.startswith('202403'):
            # Append the qualifying dir element to the new XML tree
            qualifying_root.append(dir_elem)

# Write the new XML tree to a file
qualifying_tree = ET.ElementTree(qualifying_root)
qualifying_tree.write("qualifying_dirs.xml", encoding="utf-8", xml_declaration=True)
