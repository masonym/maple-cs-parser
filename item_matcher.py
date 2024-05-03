import xml.etree.ElementTree as ET
from datetime import datetime
from packages import parse_xml

'''

Script to parse sales data and match itemIDs to string name & descriptions.

'''

def upcoming_sales():
    # This script parses a dumped Commodity.img to XML 
    # For every dir in the XML, find ones that are upcoming
    # Use current month to find any Dirs with term_start values of that month

    # Load the XML file
    tree = ET.parse('Etc.Commodity.img.xml')
    root = tree.getroot()

    # Create a new XML tree for qualifying dirs
    qualifying_root = ET.Element("root")

    now = datetime.now()
    curr_day = now.strftime("%Y%m%d")

    # Iterate over all dir elements
    for dir_elem in root.findall('.//dir'):
        # Check if the dir element has a child element with name "termStart"
        term_start_elem = dir_elem.find("./int32[@name='termStart']")
        if term_start_elem is not None:
            term_start_value = term_start_elem.get('value')
            # Check if termStart value is in the future or not
            if (term_start_value >= curr_day):
                # Append the qualifying dir element to the new XML tree
                qualifying_root.append(dir_elem)

    # Write the new XML tree to a file
    qualifying_tree = ET.ElementTree(qualifying_root)
    output = "qualifying_dirs.xml"
    qualifying_tree.write(output, encoding="utf-8", xml_declaration=True)
    print(f"Wrote contents to {output}")
    return output

def sort_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    sorted_elements = sorted(root, key=lambda x: int(x.find("int32[@name='termStart']").get("value")))

    root.clear()

    # Append the sorted elements back to the root
    for element in sorted_elements:
        root.append(element)

    # Write the sorted XML to the file
    tree.write(file)

def search_nested_xml_for_dir_by_name(root, item_id):
    """
    Search nested XML root for a directory element by name.
    
    Parameters:
        root (Element): XML root element to start the search from.
        item_id (str): ID of the item to search for.
    
    Returns:
        Element or None: XML element with the matching name, or None if not found.
    """
    return root.find(f".//dir[@name='{item_id}']")

def process_qualifying_dirs(qualifying_dirs):
    tree_original = ET.parse('qualifying_dirs.xml')
    root_original = tree_original.getroot()
    item_info = {}

    # parse the string XML files
    tree_cash = ET.parse('./strings/cash.xml')
    tree_eqp = ET.parse('./strings/equips.xml')
    tree_pet = ET.parse('./strings/pet.xml')
    root_cash = tree_cash.getroot()
    root_eqp = tree_eqp.getroot()
    root_pet = tree_pet.getroot()



    for dir_element in root_original.findall('dir'):
        # get the value of the 'ItemId' attribute from commodity data
        item_id = dir_element.find("int32[@name='ItemId']").get('value')
        price = dir_element.find("int32[@name='Price']").get('value')
        count = dir_element.find("int32[@name='Count']").get('value')
        discount = dir_element.find("int32[@name='discount']").get('value') if dir_element.find("int32[@name='discount']") is not None else "0"
        original_price = dir_element.find("int32[@name='originalPrice']").get('value') if dir_element.find("int32[@name='originalPrice']") is not None else "0"
        game_world = dir_element.find("string[@name='gameWorld']").get('value')
        period = dir_element.find("int32[@name='Period']").get('value')
        term_start_element = dir_element.find("int32[@name='termStart']")
        if term_start_element is not None:
            term_start = term_start_element.get('value')
            term_start_f = datetime.strptime(term_start, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')
        else: 
            term_start = ""
        term_end_element = dir_element.find("int32[@name='termEnd']")
        if term_end_element is not None:
            term_end = term_end_element.get('value')
            term_end_f = datetime.strptime(term_end, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')
        else:
            term_end = ""
        
        ''' Useless for now
        for key, value in packages.items():
            if item_id == key:
                package_contents[key] = value
        '''

        # search through all XML files for the corresponding Item ID
        corresponding_dir = None
        for root in [root_cash, root_eqp, root_pet]:
            corresponding_dir = search_nested_xml_for_dir_by_name(root, item_id)
            if corresponding_dir is not None:
                break
        

        if corresponding_dir is not None:
            # Get the name string
            name_element = corresponding_dir.find("string[@name='name']")
            name = name_element.get('value') if name_element is not None else "Name not found"
            
            # Get the description string
            desc_element = corresponding_dir.find("string[@name='desc']")
            description = desc_element.get('value') if desc_element is not None else ""
            description = description.replace("#c","").replace("\\n","\n").replace("#","")
            

            
            item_info[item_id] = {'name': name, 'count': count, 'description': description, 'price': price, 'discount': discount, 'originalPrice': original_price, 'termStart': term_start_f, 'termEnd': term_end_f, 'gameWorld': game_world, 'period': period}

    ## loop for getting package contents
    ## for now this does nothing. i have no idea what the IDs returned for package contents are.
    '''
    for key, value in package_contents.items():
        for elem in value:
            item_id = elem
            corresponding_dir = None
            for root in [root_cash, root_eqp, root_pet]:
                corresponding_dir = search_nested_xml_for_dir_by_name(root, item_id)
                if corresponding_dir is not None:
                    break
            

            if corresponding_dir is not None:
                # Get the name string
                name_element = corresponding_dir.find("string[@name='name']")
                name = name_element.get('value') if name_element is not None else "Name not found"
                
                # Get the description string
                desc_element = corresponding_dir.find("string[@name='desc']")
                description = desc_element.get('value') if desc_element is not None else ""

                item_info[item_id] = {'Package': key, 'name': name, 'description': description}        
    '''
    
    return item_info

def main():
    qualifying_dirs = upcoming_sales()
    sort_xml(qualifying_dirs)
    item_info = process_qualifying_dirs(qualifying_dirs)
    with open("CashShopSales.xml", "w") as file:
        for item_id, info in item_info.items():
            output = "---\n"
            if info['name'] != "":
                output += f"Name: {info['name']}"
                if int(info['count']) > 1:
                    output += f" ({info['count']})\n"
                else:
                    output += "\n"
            if info['description'] != "":
                output += f"Description: {info['description']}\n"
            if info['period'] != "":
                output += f"Duration: "
                output += f"{info['period']} days\n\n" if info['period'] != "0" else f"Permanent\n\n"
            if info['price'] != "":
                output += f"Price: {int(info['price']):,} NX"
                if info['discount'] == "1":
                    output += f" (was {int(info['originalPrice']):,} NX)\n"
                else:
                    output += "\n"
            if info['termStart'] != "":
                output += f"Start Date: {info['termStart']}\n"
            if info['termEnd'] != "":
                output += f"End Date: {info['termEnd']}\n"
            if info['gameWorld'] != "":
                if info['gameWorld'] == "45/46/70":
                    output += f"Heroic Servers Only\n"
                elif info['gameWorld'] == "0/1/17/18/30/48/49":
                    output += f"Interactive Servers Only\n"
                else: output += f"Heroic & Interactive Servers\n"
            if output != "":
                file.write(output + "\n")

    print("Saved as CashShopSales.txt")

if __name__ == "__main__":
    main()