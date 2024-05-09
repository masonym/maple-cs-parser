import json
from data_parsing import parse_xml_files, search_nested_xml_for_dir_by_name
from data_processing import upcoming_sales, sort_xml, package_dict_creator, process_qualifying_dirs
from image_handling import get_images
from utils import format_description

def main():
    root_commodity, root_cash, root_eqp, root_pet, root_package_names, root_package_contents = parse_xml_files()
    
    qualifying_dirs = upcoming_sales(root_commodity)
    sort_xml(qualifying_dirs, 'termStart')
    
    package_dict = package_dict_creator(qualifying_dirs, root_package_names, root_package_contents)
    
    item_info = process_qualifying_dirs(qualifying_dirs, package_dict, root_commodity, root_cash, root_eqp, root_pet, search_nested_xml_for_dir_by_name)
    
    get_images(item_info)

    with open('item_data.json', 'w') as f:
        json.dump(item_info, f, indent=4)

    return item_info

if __name__ == "__main__":
    main()