import xml.etree.ElementTree as ET
from datetime import datetime
from packages import parse_xml

def search_xml_for_dir_by_name(root, dir_name):
    """
    Search XML root for a directory element by name.
    
    Parameters:
        root (Element): XML root element to start the search from.
        dir_name (str): Name of the directory to search for.
    
    Returns:
        Element or None: XML element with the matching name, or None if not found.
    """
    return root.find(f".//dir[@name='{dir_name}']")

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

def process_qualifying_dirs():
    tree_original = ET.parse('qualifying_dirs.xml')
    root_original = tree_original.getroot()
    item_info = {}

    # Parse the string XML files
    tree_cash = ET.parse('./strings/cash.xml')
    tree_eqp = ET.parse('./strings/equips.xml')
    tree_pet = ET.parse('./strings/pet.xml')
    root_cash = tree_cash.getroot()
    root_eqp = tree_eqp.getroot()
    root_pet = tree_pet.getroot()



    for dir_element in root_original.findall('dir'):
        # Get the value of the 'ItemId' attribute from commodity data
        item_id = dir_element.find("int32[@name='ItemId']").get('value')
        price = dir_element.find("int32[@name='Price']").get('value')
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
        

        for key, value in packages.items():
            if item_id == key:
                package_contents[key] = value
        # Search through all XML files for the corresponding Item ID
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

            
            item_info[item_id] = {'name': name, 'description': description, 'price': price, 'termStart': term_start_f, 'termEnd': term_end_f}

    ## loop for getting package contents
    ## for now this does nothing. i have no idea what the IDs returned for package contents are.
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

    return item_info


# Example usage:

packages_dir = './strings/packages.xml'
packages = parse_xml(packages_dir)
package_contents = {}

item_info = process_qualifying_dirs()
with open("CashShopSales.txt", "w") as file:
    for item_id, info in item_info.items():
        output = ""
        if info['name'] != "":
            output += f"Name: {info['name']}\n"
        if info['description'] != "":
            output += f"Description: {info['description']}\n"
        if info['price'] != "":
            output += f"Price: {info['price']} NX\n"
        if info['termStart'] != "":
            output += f"Start Date: {info['termStart']}\n"
        if info['termEnd'] != "":
            output += f"End Date: {info['termEnd']}\n"
        if output != "":
            file.write(output + "\n")

