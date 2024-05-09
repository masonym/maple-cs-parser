import xml.etree.ElementTree as ET
from datetime import datetime

# Paths to XML source files
CASH_XML = '../dumped_wz/String.wz/Cash.img.xml'
EQUIPS_XML = '../dumped_wz/String.wz/Eqp.img.xml'
PET_XML = '../dumped_wz/String.wz/Pet.img.xml'
COMMODITY_XML = '../dumped_wz/Etc.wz/Commodity.img.xml'
PACKAGE_NAMES_XML = '../dumped_wz/Item.wz/Special/0910.img.xml'
PACKAGE_CONTENTS_XML = '../dumped_wz/Etc.wz/CashPackage.img.xml'

def parse_xml_files():
    """
    Parse the XML files and return the root elements.
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

def search_nested_xml_for_dir_by_name(root, item_id):
    """
    Search nested XML root for a directory element by name.
    """
    return root.find(f".//imgdir[@name='{item_id}']")