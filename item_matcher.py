import xml.etree.ElementTree as ET
from datetime import datetime
import shutil
import os.path

'''

Script to parse sales data and match itemIDs to string name & descriptions.

'''
# Global variables
CASH_XML = './dumped_wz/String.wz/Cash.img.xml'
EQUIPS_XML = './dumped_wz/String.wz/Eqp.img.xml'
PET_XML = './dumped_wz/String.wz/Pet.img.xml'
COMMODITY_XML = './dumped_wz/Etc.wz/Commodity.img.xml'
PACKAGE_NAMES_XML = './dumped_wz/Item.wz/Special/0910.img.xml'
PACKAGE_CONTENTS_XML = './dumped_wz/Etc.wz/CashPackage.img.xml'

def parse_xml_files():
    """
    Parse the XML files and return the root elements.
    Returns:
    #1 - commodity strings
    #2 - cash strings
    #3 - eqp strings
    #4 - pet strings
    #5 - package names
    #6 - package contents
    """
    tree_commodity = ET.parse(COMMODITY_XML)
    tree_cash = ET.parse(CASH_XML)
    tree_eqp = ET.parse(EQUIPS_XML)
    tree_pet = ET.parse(PET_XML)
    tree_package_names = ET.parse(PACKAGE_NAMES_XML)
    tree_package_contents = ET.parse(PACKAGE_CONTENTS_XML)

    return (
        tree_commodity.getroot(),
        tree_cash.getroot(),
        tree_eqp.getroot(),
        tree_pet.getroot(),
        tree_package_names.getroot(),
        tree_package_contents.getroot()
    )

def upcoming_sales(root_commodity):
    # This script parses a dumped Commodity.img to XML 
    # For every dir in the XML, find ones that are upcoming
    # Use current month to find any Dirs with term_start values of that month

    # Create a new XML tree for qualifying dirs
    qualifying_root = ET.Element("root")

    now = datetime.now()
    curr_day = now.strftime("%Y%m%d")

    # Iterate over all dir elements
    for dir_elem in root_commodity.findall('.//imgdir'):
        # Check if the dir element has a child element with name "termStart"
        term_end_elem = dir_elem.find("./int[@name='termEnd']")
        # Check if termEnd value is in the past or not
        if term_end_elem is not None and term_end_elem.get('value') >= curr_day:
            # Append the qualifying dir element to the new XML tree
            qualifying_root.append(dir_elem)

    
    qualifying_tree = ET.ElementTree(qualifying_root)

    return qualifying_tree

def sort_xml(tree, sort_by):
    '''
    Sort an XML tree by passed element
    '''
    root = tree.getroot()

    sorted_elements = sorted(root, key=lambda x: int(x.find(f"int[@name='{sort_by}']").get("value")))

    root.clear()

    # Append the sorted elements back to the root
    for element in sorted_elements:
        root.append(element)

    return tree

def search_nested_xml_for_dir_by_name(root, item_id):
    """
    Search nested XML root for a directory element by name.
    
    Parameters:
        root (Element): XML root element to start the search from.
        item_id (str): ID of the item to search for.
    
    Returns:
        Element or None: XML element with the matching name, or None if not found.
    """
    return root.find(f".//imgdir[@name='{item_id}']")

def package_dict_creator(qualified_tree, root_package_names, root_package_contents):
    root = qualified_tree.getroot()

    # make package dir for storing data
    # contents will be an array of SN IDs
    package_dict = {}

    # get package names
    for dir_element in root.findall('imgdir'):
        item_id = dir_element.find("int[@name='ItemId']").get('value')
        if item_id.startswith("910"):
            # for dir_element_2 in root_package_names:
            package = root_package_names.find(f"imgdir[@name='{item_id}']")
            package_id = package.attrib['name']
            package_dict[package_id] = {}
            package_dict[package_id]["name"] = package.find("string[@name='name']").get('value')
            package_dict[package_id]["description"] = package.find("string[@name='desc']").get('value').replace("#c","").replace("\\n","\n").replace("#","") if package.find("string[@name='desc']") is not None else ""

            for dir_element in root_package_contents.findall('imgdir'):
                if package_id == dir_element.attrib['name']:
                    package_dict[package_id]["contents"] = [int_element.get('value') for int_element in dir_element.findall('.//int')]

    
    # return nested dictionaries
    return package_dict

def package_contents_parser(package_dict, item_id, root_commodity):
    item_ids = {}
    item_ids[item_id] = {}
    array = package_dict[item_id].get("contents")
    for idx, sn in enumerate(array):
        for dir_element in root_commodity.findall('.//imgdir'):
            sn_elem = dir_element.find('int[@name="SN"]')
            if sn_elem is not None and sn_elem.get('value') == sn:
                item_id_element = dir_element.find('int[@name="ItemId"]')
                item_count_element = dir_element.find('int[@name="Count"]')
                if item_id_element is not None:
                    item_ids[item_id][idx] = {
                        'itemID': item_id_element.get('value'),
                        'count': item_count_element.get('value')
                    }
                break
    return item_ids

def process_qualifying_dirs(qualified_tree, package_dict, root_commodity, root_cash, root_eqp, root_pet):
    root_qualified = qualified_tree.getroot()
    item_info = {}

    for dir_element in root_qualified.findall('imgdir'):
        package_contents = {}
        # get the value of the 'ItemId' attribute from commodity data

        sn_id = dir_element.find("int[@name='SN']").get('value')
        item_id = dir_element.find("int[@name='ItemId']").get('value')
        price = dir_element.find("int[@name='Price']").get('value')
        count = dir_element.find("int[@name='Count']").get('value')
        discount = dir_element.find("int[@name='discount']").get('value') if dir_element.find("int[@name='discount']") is not None else "0"
        original_price = dir_element.find("int[@name='originalPrice']").get('value') if dir_element.find("int[@name='originalPrice']") is not None else "0"
        game_world = dir_element.find("string[@name='gameWorld']").get('value')
        period = dir_element.find("int[@name='Period']").get('value')

        term_start_element = dir_element.find("int[@name='termStart']")
        term_start = term_start_element.get('value')
        term_start_f = datetime.strptime(term_start, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')

        term_end_element = dir_element.find("int[@name='termEnd']")
        term_end = term_end_element.get('value')
        term_end_f = datetime.strptime(term_end, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')

        # search through all XML files for the corresponding Item ID
        corresponding_dir = None
        if item_id.startswith("910"):
            # stuff
            contents = package_contents_parser(package_dict, item_id, root_commodity)
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
                        description = desc_element.get('value') if desc_element is not None else None
                        description = description.replace("#c","").replace("\\n","\n").replace("#","") if description is not None else None

                        package_contents[odx][idx] = {'itemID': sub_item_id, 'name': name, 'description': description, 'count': count}

                    
                    
            item_info[item_id] = {'itemID': item_id, 'name': package_dict[item_id].get('name'), 'description': package_dict[item_id].get('description'),
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
            description = desc_element.get('value') if desc_element is not None else None
            description = description.replace("#c","").replace("\\n","\n").replace("#","") if description is not None else None
            
            # pets are listed as permanent because the item itself is permanent
            # but the magic duration is not permanent
            # life info comnes from {item_id}.img.xml form the <int name="life" value=x"> dir
            if item_id.startswith("500") and price == "4900":
                pet_path = f"./dumped_wz/Item.wz/Pet/{item_id}.img.xml"
                pet_info_tree = ET.parse(pet_path)
                pet_info_root = pet_info_tree.getroot()
                life_val = pet_info_root.find(".//int[@name='life']").attrib['value']
                period = life_val

            
            item_info[sn_id] = {'itemID': item_id, 'name': name, 'count': count, 'description': description, 'price': price, 'discount': discount, 'originalPrice': original_price, 'termStart': term_start_f, 'termEnd': term_end_f, 'gameWorld': game_world, 'period': period}

    return item_info

def get_images(item_dict):

    """"
    maybe theres a better way to do this idk
    could probably do this in an object-oriented way? 
    object's range = prefix, idk

    cash:
    501-599

    pet:
    500xx



    face: 002-005
    hat: 100
    accessory: 101, 102, 103, 112 to 119
    coat: 104
    longcoat: 105
    pants: 106
    shoes: 107
    glove: 108
    shield: 109
    cape: 110
    ring: 111
    weapon: 121 to 171
    android: 166-167
    """




    # sn_id = SN (key)
    # info = dict entry 
    for sn_id, info in item_dict.items():
        item_id = info.get('itemID')
        prefix = int(str(info.get('itemID'))[:3])

        if prefix in range(2, 6):
            img_path = f"./dumped_wz/Character/Face/_Canvas/{item_id}.img/info/icon.png"
        elif prefix == 100:
            img_path = f"./dumped_wz/Character/Cap/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix in [101, 102, 103] or prefix in range(112, 120):
            img_path = f"./dumped_wz/Character/Accessory/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 104:
            img_path = f"./dumped_wz/Character/Coat/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 105:
            img_path = f"./dumped_wz/Character/Longcoat/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 106:
            img_path = f"./dumped_wz/Character/Pants/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 107:
            img_path = f"./dumped_wz/Character/Shoes/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 108:
            img_path = f"./dumped_wz/Character/Glove/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 109:
            img_path = f"./dumped_wz/Character/Shield/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 110:
            img_path = f"./dumped_wz/Character/Cape/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 111:
            img_path = f"./dumped_wz/Character/Ring/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 180:
            img_path = f"./dumped_wz/Character/PetEquip/_Canvas/0{item_id}.img/info/icon.png"
        # weapon
        elif prefix in range(121, 172):
            xml_path = f"./dumped_wz/Character/Weapon/0{item_id}.img.xml"
            wep_tree = ET.parse(xml_path)
            root = wep_tree.getroot()
            icon_canvas = root.find(".//canvas[@name='icon']")
            outlink_value = icon_canvas.find("string[@name='_outlink']").attrib['value']
            img_path = f"./dumped_wz/{outlink_value}.png"
        # android
        elif prefix in [166, 167]:
            img_path = f"./dumped_wz/Character/Android/_Canvas/0{item_id}.img/info/icon.png"
        # pets
        elif prefix == 500:
            img_path = f"./dumped_wz/Item.wz/Pet/{item_id}.img/info/icon.png"
        # cash items
        elif prefix in range(500, 600):
            img_path = f"./dumped_wz/Item.wz/Cash/0{prefix}.img/0{item_id}/info/icon.png"
        # packages
        elif prefix >= 900:
            img_path = f"./dumped_wz/Item.wz/Special/0{prefix}.img/{item_id}/icon.png"
            for package_id, items in info['packageContents'].items():
                # recursively call image getter on package contents dict
                get_images(items)

        else:
            img_path = f"Unknown file path for item ID: {item_id}"
    

        dest_file = f'./images/{item_id}.png'

        # put item icon into images folder if img doesnt already exist
        if not os.path.isfile(dest_file):
            shutil.copy(img_path, dest_file)
        
        


def main():
    root_commodity, root_cash, root_eqp, root_pet, root_package_names, root_package_contents = parse_xml_files()
    qualifying_dirs = upcoming_sales(root_commodity)
    sort_by = 'termStart' # change this if you want to change the sort
    sort_xml(qualifying_dirs, sort_by)
    package_dict = package_dict_creator(qualifying_dirs, root_package_names, root_package_contents)
    item_info = process_qualifying_dirs(qualifying_dirs, package_dict, root_commodity, root_cash, root_eqp, root_pet)
    get_images(item_info)

    with open("CashShopSales.txt", "w") as file:
        for item_id, info in item_info.items():
            output_lines = []
            output_lines.append("---")
            if info.get('name') != "":
                name_line = f"Name: {info['name']}"
                if int(info.get('count', 0)) > 1:
                    name_line += f" ({info['count']})"
                output_lines.append(name_line)

            if info.get('description'):
                output_lines.append(f"Description: {info['description']}")

            if info.get('period') != "":
                duration_line = "Duration: "
                duration_line += f"{info['period']} days" if info['period'] != "0" else "Permanent"
                output_lines.append(duration_line)
                output_lines.append("")

            ## CURRENTLY this does a funky workaround to display the currency
            ## but i've learned that items sold in Mesos actually have an SN id starting with `87`
            ## so we can use that to our advantage later. probably will be nice for the website to categorize things
            ## but for now this remains.
            if info.get('price') != "":
                currency = "Mesos" if int(info['price']) > 1000001 else "NX"
                price_line = f"Price: {int(info['price']):,} {currency}"
                if info.get('discount') == "1":
                    price_line += f" (was {int(info['originalPrice']):,} {currency})"
                output_lines.append(price_line)

            if 'packageContents' in info:
                output_lines.append("\nPackage Contents:")
                curr_package = info['packageContents'].get(f'{item_id}')
                for idx, item in enumerate(curr_package):
                    content_lines = []
                    if curr_package[idx].get('name') != "":
                        content_lines.append(f"* Name: {curr_package[idx]['name']}")
                        if int(curr_package[idx].get('count', 0)) > 1:
                            content_lines[-1] += f" ({curr_package[idx]['count']})"
                    if curr_package[idx].get('description'):
                        content_lines.append(f"  * Description: {curr_package[idx]['description']}")
                    output_lines.extend(content_lines)

            if info.get('termStart') != "":
                output_lines.append(f"\nStart Date: {info['termStart']}")

            if info.get('termEnd') != "":
                output_lines.append(f"End Date: {info['termEnd']}")
                output_lines.append("")

            if info.get('gameWorld') != "":
                if info['gameWorld'] == "45/46/70":
                    output_lines.append("Heroic Servers Only")
                elif info['gameWorld'] == "0/1/17/18/30/48/49":
                    output_lines.append("Interactive Servers Only")
                else:
                    output_lines.append("Heroic & Interactive Servers")

            if output_lines:
                output = "\n".join(output_lines)
                file.write(output + "\n\n")

    print("Saved as CashShopSales.txt")
if __name__ == "__main__":
    main()