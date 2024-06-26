import xml.etree.ElementTree as ET
from datetime import datetime
from utils import format_description, get_gender_from_id
from image_handling import PATH_PREF_ITEM

def upcoming_sales(root_commodity):
    qualifying_root = ET.Element("root")
    now = datetime.now()
    curr_day = now.strftime("%Y%m%d")

    for dir_elem in root_commodity.findall('.//imgdir'):
        term_start_elem = dir_elem.find("./int[@name='termStart']")
        term_end_elem = dir_elem.find("./int[@name='termEnd']")
        if None not in (term_start_elem, term_end_elem):
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

def package_contents_parser(package_dict, item_id, root_commodity):
    item_ids = {item_id: {}}
    array = package_dict[item_id].get("contents", [])
    
    dir_elements = {(dir_element.find('int[@name="SN"]').get('value')): dir_element for dir_element in root_commodity.findall('.//imgdir')}
    
    for idx, sn in enumerate(array):
        dir_element = dir_elements.get(str(sn))
        if dir_element is not None:
            item_id_element = dir_element.find('int[@name="ItemId"]')
            item_count_element = dir_element.find('int[@name="Count"]')
            item_period_element = dir_element.find('int[@name="Period"]')
            if item_id_element is not None:
                item_ids[item_id][idx] = {
                    'itemID': item_id_element.get('value'),
                    'count': item_count_element.get('value') if item_count_element is not None else '1',                    
                    'period': item_period_element.get('value')
                }
                # need to check if package item is a pet, so that we can get the proper duration
                if item_id_element.get('value').startswith("500"):
                    pet_path = f"{PATH_PREF_ITEM}/Pet/{item_id_element.get('value')}.img.xml"
                    pet_info_tree = ET.parse(pet_path)
                    pet_info_root = pet_info_tree.getroot()
                    life_val = pet_info_root.find(".//int[@name='life']").attrib['value']
                    item_ids[item_id][idx]['period'] = life_val
    return item_ids

def process_qualifying_dirs(qualified_tree, package_dict, root_commodity, root_cash, root_eqp, root_pet, search_nested_xml_for_dir_by_name):
    root_qualified = qualified_tree.getroot()
    item_info = {}

    for dir_element in root_qualified.findall('imgdir'):
        package_contents = {}
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
            for odx, items in contents.items():
                package_contents[odx] = {}
                for idx, item_data in items.items():
                    sub_item_id = item_data['itemID']
                    item_count = item_data['count']
                    period = item_data['period']

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

                        gender = get_gender_from_id(sub_item_id)
                        if gender == 0:
                            name += " (Male)"
                        elif gender == 1:
                            name += " (Female)"
                        
                        package_contents[odx][idx] = {'itemID': sub_item_id, 'name': name, 'description': description, 'count': item_count, 'period': period}
                    
            item_info[item_id] = {
                'itemID': item_id,
                'name': package_dict[item_id].get('name'),
                'description': package_dict[item_id].get('description'),
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
        for root in [root_cash, root_eqp, root_pet]:
            corresponding_dir = search_nested_xml_for_dir_by_name(root, item_id)
            if corresponding_dir is not None:
                break
            
        if corresponding_dir is not None:
            name_element = corresponding_dir.find("string[@name='name']")
            name = name_element.get('value') if name_element is not None else "Name not found"
            desc_element = corresponding_dir.find("string[@name='desc']")
            description = format_description(desc_element.get('value')) if desc_element is not None else None

            gender = get_gender_from_id(item_id)
            if gender == 0:
                name += " (Male)"
            elif gender == 1:
                name += " (Female)"
            
            if item_id.startswith("500"):
                pet_path = f"{PATH_PREF_ITEM}/Pet/{item_id}.img.xml"
                pet_info_tree = ET.parse(pet_path)
                pet_info_root = pet_info_tree.getroot()
                life_val = pet_info_root.find(".//int[@name='life']").attrib['value']
                period = life_val
            
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