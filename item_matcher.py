import xml.etree.ElementTree as ET
from datetime import datetime

# globals
tree_cash = ET.parse('./strings/cash.xml')
tree_eqp = ET.parse('./strings/equips.xml')
tree_pet = ET.parse('./strings/pet.xml')
root_cash = tree_cash.getroot()
root_eqp = tree_eqp.getroot()
root_pet = tree_pet.getroot()
'''

Script to parse sales data and match itemIDs to string name & descriptions.

'''

def upcoming_sales():
    # This script parses a dumped Commodity.img to XML 
    # For every dir in the XML, find ones that are upcoming
    # Use current month to find any Dirs with term_start values of that month

    # Load the XML file
    tree = ET.parse('./strings/commodity.xml')
    root = tree.getroot()

    # Create a new XML tree for qualifying dirs
    qualifying_root = ET.Element("root")

    now = datetime.now()
    curr_day = now.strftime("%Y%m")

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
    # TODO:
    # we don't need to save this as a file, we can just pass it.
    # fix later.
    
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

def package_dict_creator(qualifying_dirs):
    tree = ET.parse(qualifying_dirs)
    root = tree.getroot()

    tree_package_names = ET.parse('./strings/package_names.xml')
    root_package_names = tree_package_names.getroot()

    tree_package_contents = ET.parse('./strings/package_contents.xml')
    root_package_contents = tree_package_contents.getroot()

    # make package dir for storing data
    # contents will be an array of SN IDs
    package_dict = {
        # "packageID": "",
        # "name": "",
        # "description": "",
        # "contents": ""
    }

    # get package names
    for dir_element in root.findall('dir'):
        item_id = dir_element.find("int32[@name='ItemId']").get('value')
        if item_id.startswith("910"):
            # for dir_element_2 in root_package_names:
            package = root_package_names.find(f"dir[@name='{item_id}']")
            package_id = package.attrib['name']
            package_dict[package_id] = {}
            package_dict[package_id]["name"] = package.find("string[@name='name']").get('value')
            package_dict[package_id]["description"] = package.find("string[@name='desc']").get('value').replace("#c","").replace("\\n","\n").replace("#","") if package.find("string[@name='desc']") is not None else ""

            for dir_element in root_package_contents.findall('dir'):
                contents = []
                if package_id == dir_element.attrib['name']:
                    for int32_element in dir_element.findall('.//int32'):
                        value = int32_element.get('value')
                        contents.append(value)
                    package_dict[package_id]["contents"] = contents
    
    # return nested dictionaries
    return package_dict

def package_contents_parser(package_dict, item_id):
    # something = an entry from our dictionary
    # or maybe pass in dictionary and item_id?
    tree = ET.parse('./strings/commodity.xml')
    root = tree.getroot()
    item_ids = {}
    item_ids[item_id] = {}
    array = package_dict[item_id].get("contents")
    for idx, sn in enumerate(array):
        for dir_element in root.findall('.//dir'):
            sn_elem = dir_element.find('int32[@name="SN"]')
            if sn_elem is not None and sn_elem.get('value') == sn:
                item_id_element = dir_element.find('int32[@name="ItemId"]')
                item_count_element = dir_element.find('int32[@name="Count"]')
                if item_id_element is not None:
                    item_ids[item_id][idx] = {
                        'itemID': item_id_element.get('value'),
                        'count': item_count_element.get('value')
                    }
                break
    return item_ids



def process_qualifying_dirs(qualifying_dirs, package_dict):
    tree_original = ET.parse(qualifying_dirs)
    root_original = tree_original.getroot()
    item_info = {}
    package_contents = {}
    # parse the string XML files


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

        # search through all XML files for the corresponding Item ID
        corresponding_dir = None
        if item_id.startswith("910"):
            # stuff
            contents = package_contents_parser(package_dict, item_id)
            for odx, items in contents.items():
                package_contents[odx] = {}
                for idx, item_data in items.items():
                    sub_item_id = item_data['itemID']
                    count = item_data['count']

                    for root in [root_cash, root_eqp, root_pet]:
                        corresponding_dir = search_nested_xml_for_dir_by_name(root, sub_item_id)
                        if corresponding_dir is not None:
                            break
                    if corresponding_dir is not None:

                        name_element = corresponding_dir.find("string[@name='name']")
                        name = name_element.get('value') if name_element is not None else "Name not found"
                        
                        # Get the description string
                        desc_element = corresponding_dir.find("string[@name='desc']")
                        description = desc_element.get('value') if desc_element is not None else ""
                        description = description.replace("#c","").replace("\\n","\n").replace("#","")

                        package_contents[odx][idx] = {'name': name, 'description': description, 'count': count}

                    
                    
            item_info[item_id] = {'name': package_dict[item_id].get('name'), 'description': package_dict[item_id].get('description'),
                                  'count': count, 'price': price, 'discount': discount, 'originalPrice': original_price,
                                  'termStart': term_start_f, 'termEnd': term_end_f, 'gameWorld': game_world, 'period': period,
                                  'packageContents': package_contents
                                  }
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
            
            if item_id.startswith("500") and price == "4900":
                period = "90"

            
            item_info[item_id] = {'name': name, 'count': count, 'description': description, 'price': price, 'discount': discount, 'originalPrice': original_price, 'termStart': term_start_f, 'termEnd': term_end_f, 'gameWorld': game_world, 'period': period}

    return item_info

def main():
    qualifying_dirs = upcoming_sales()
    sort_xml(qualifying_dirs)
    package_dict = package_dict_creator(qualifying_dirs)
    item_info = process_qualifying_dirs(qualifying_dirs, package_dict)


    with open("CashShopSales.txt", "w") as file:
        for item_id, info in item_info.items():
            output = "---\n"
            if info['name'] != "":
                output += f"Name: {info['name']}"
                if int(info['count']) != "":
                    output += f" ({info['count']})\n" if int(info['count']) > 1 else "\n"
            if info['description'] != "":
                output += f"Description: {info['description']}\n"
            if info['period'] != "":
                output += "Duration: "
                output += f"{info['period']} days\n\n" if info['period'] != "0" else "Permanent\n\n"
            if info['price'] != "":
                currency = "Mesos" if int(info['price']) > 1000001 else "NX"
                output+= f"Price: {int(info['price']):,} {currency}"
                if info['discount'] == "1":
                    output += f" (was {int(info['originalPrice']):,} {currency})\n"
                else:
                    output += "\n"
            if 'packageContents' in info:
                output+= "\nPackage Contents: \n"
                curr_package = info['packageContents'].get(f'{item_id}')
                for idx, item in enumerate(curr_package):
                    output+= f"* Name: {curr_package[idx].get('name')}"
                    if int(curr_package[idx].get('count')) > 1:
                        output+= f" ({curr_package[idx].get('count')})\n"
                    else:
                        output+= "\n"
                    output+= f"* Description: {curr_package[idx].get('description')}\n\n" if curr_package[idx].get('description') != "" else ""
            if info['termStart'] != "":
                output += f"\nStart Date: {info['termStart']}\n"
            if info['termEnd'] != "":
                output += f"End Date: {info['termEnd']}\n\n"
            if info['gameWorld'] != "":
                if info['gameWorld'] == "45/46/70":
                    output += "Heroic Servers Only\n"
                elif info['gameWorld'] == "0/1/17/18/30/48/49":
                    output += "Interactive Servers Only\n"
                else:
                    output += "Heroic & Interactive Servers\n"
            if output != "":
                file.write(output + "\n")

    print("Saved as CashShopSales.txt")

if __name__ == "__main__":
    main()