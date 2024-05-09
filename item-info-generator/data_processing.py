import xml.etree.ElementTree as ET
from datetime import datetime
from utils import format_description  # Import the utility function

def package_contents_parser(package_dict, item_id, root_commodity):
    """
    Parse the contents of each package using the package dictionary and commodity data.
    """
    item_ids = {}
    item_ids[item_id] = {}
    array = package_dict[item_id].get("contents", [])
    
    for idx, sn in enumerate(array):
        for dir_element in root_commodity.findall('.//imgdir'):
            sn_elem = dir_element.find('int[@name="SN"]')
            if sn_elem is not None and sn_elem.get('value') == str(sn):
                item_id_element = dir_element.find('int[@name="ItemId"]')
                item_count_element = dir_element.find('int[@name="Count"]')
                if item_id_element is not None:
                    item_ids[item_id][idx] = {
                        'itemID': item_id_element.get('value'),
                        'count': item_count_element.get('value') if item_count_element is not None else '1'
                    }
                break
    return item_ids

def upcoming_sales(root_commodity):
    qualifying_root = ET.Element("root")
    now = datetime.now()
    curr_day = now.strftime("%Y%m%d")

    for dir_elem in root_commodity.findall('.//imgdir'):
        term_end_elem = dir_elem.find("./int[@name='termEnd']")
        if term_end_elem is not None and term_end_elem.get('value') >= curr_day:
            qualifying_root.append(dir_elem)

    return ET.ElementTree(qualifying_root)

def sort_xml(tree, sort_by):
    root = tree.getroot()
    sorted_elements = sorted(root, key=lambda x: int(x.find(f"int[@name='{sort_by}']").get("value")))
    root.clear()
    for element in sorted_elements:
        root.append(element)
    return tree

def package_dict_creator(qualified_tree, root_package_names, root_package_contents):
    root = qualified_tree.getroot()
    package_dict = {}

    for dir_element in root.findall('imgdir'):
        item_id = dir_element.find("int[@name='ItemId']").get('value')
        if item_id.startswith("910"):
            package = root_package_names.find(f"imgdir[@name='{item_id}']")
            if package:
                package_id = package.attrib['name']
                package_dict[package_id] = {
                    "name": package.find("string[@name='name']").get('value'),
                    "description": format_description(package.find("string[@name='desc']").get('value')) if package.find("string[@name='desc']") is not None else ""
                }

                for dir_element in root_package_contents.findall('imgdir'):
                    if package_id == dir_element.attrib['name']:
                        package_dict[package_id]["contents"] = [int(int_element.get('value')) for int_element in dir_element.findall('.//int')]
    return package_dict

def process_qualifying_dirs(qualified_tree, package_dict, root_commodity, root_cash, root_eqp, root_pet, search_nested_xml_for_dir_by_name):
    root_qualified = qualified_tree.getroot()
    item_info = {}

    for dir_element in root_qualified.findall('imgdir'):
        sn_id = dir_element.find("int[@name='SN']").get('value')
        item_id = dir_element.find("int[@name='ItemId']").get('value')
        price = dir_element.find("int[@name='Price']").get('value')
        count = dir_element.find("int[@name='Count']").get('value')
        discount = dir_element.find("int[@name='discount']").get('value') if dir_element.find("int[@name='discount']") is not None else "0"
        original_price = dir_element.find("int[@name='originalPrice']").get('value') if dir_element.find("int[@name='originalPrice']") is not None else "0"
        game_world = dir_element.find("string[@name='gameWorld']").get('value')
        period = dir_element.find("int[@name='Period']").get('value')

        term_start = dir_element.find("int[@name='termStart']").get('value')
        term_start_f = datetime.strptime(term_start, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')
        term_end = dir_element.find("int[@name='termEnd']").get('value')
        term_end_f = datetime.strptime(term_end, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')

        if item_id.startswith("910"):
            contents = package_contents_parser(package_dict, item_id, root_commodity)
            package_contents = {}
            for odx, items in contents.items():
                package_contents[odx] = {}
                for idx, item_data in items.items():
                    sub_item_id = item_data['itemID']
                    item_count = item_data['count']

                    corresponding_dir = None
                    for root in [root_cash, root_eqp, root_pet]:
                        corresponding_dir = search_nested_xml_for_dir_by_name(root, sub_item_id)
                        if corresponding_dir is not None:
                            break
                    
                    if corresponding_dir is not None:
                        name_element = corresponding_dir.find("string[@name='name']")
                        name = name_element.get('value') if name_element is not None else "Name not found"
                        desc_element = corresponding_dir.find("string[@name='desc']")
                        description = format_description(desc_element.get('value')) if desc_element is not None else None
                        
                        package_contents[odx][idx] = {'itemID': sub_item_id, 'name': name, 'description': description, 'count': item_count}
                    
            item_info[item_id] = {
                'itemID': item_id,
                'name': package_dict[item_id]['name'],
                'description': package_dict[item_id]['description'],
                'count': count,
                'price': price,
                'discount': discount,
                'originalPrice': original_price,
                'termStart': term_start_f,
                'termEnd': term_end_f,
                'gameWorld': game_world,
                'period': period,
                'packageContents': package_contents
            }
        else:
            for root in [root_cash, root_eqp, root_pet]:
                corresponding_dir = search_nested_xml_for_dir_by_name(root, item_id)
                if corresponding_dir is not None:
                    break
            
            if corresponding_dir is not None:
                name_element = corresponding_dir.find("string[@name='name']")
                name = name_element.get('value') if name_element is not None else "Name not found"
                desc_element = corresponding_dir.find("string[@name='desc']")
                description = format_description(desc_element.get('value')) if desc_element is not None else None
                
                item_info[sn_id] = {
                    'itemID': item_id,
                    'name': name,
                    'count': count,
                    'description': description,
                    'price': price,
                    'discount': discount,
                    'originalPrice': original_price,
                    'termStart': term_start_f,
                    'termEnd': term_end_f,
                    'gameWorld': game_world,
                    'period': period
                }

    return item_info