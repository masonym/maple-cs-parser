import xml.etree.ElementTree as ET
import shutil
import os
import os.path

DUMPED_WZ = '../dumped_wz'
PATH_PREF_CHAR = f"{DUMPED_WZ}/Character"
PATH_PREF_ITEM = f"{DUMPED_WZ}/Item.wz"

PREFIX_PATH_MAP = {
    range(2, 6): "Face",
    100: "Cap",
    range(101, 103): "Accessory",
    range(112, 120): "Accessory",
    104: "Coat",
    105: "Longcoat",
    106: "Pants",
    107: "Shoes",
    108: "Glove",
    109: "Shield",
    110: "Cape",
    111: "Ring",
    range(166, 167): "Android",
    180: "PetEquip",
    range(121, 172): "Weapon",
}

def get_xml_path(item_id):
    prefix = int(str(item_id)[:3])
    for key, path in PREFIX_PATH_MAP.items():
        if isinstance(key, range) and prefix in key or prefix == key:
            return f"{PATH_PREF_CHAR}/{path}/0{item_id}.img.xml"
    return None

def get_image_path(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    icon_canvas = root.find(".//canvas[@name='icon']")
    outlink_value = icon_canvas.find("string[@name='_outlink']").attrib['value']
    return f"{DUMPED_WZ}/{outlink_value}.png"

def process_item(item_id, dest_file):
    xml_path = get_xml_path(item_id)
    if xml_path and os.path.isfile(xml_path):
        img_path = get_image_path(xml_path)
    else:
        # Pets, Cash Items, and Packages
        prefix = int(str(item_id)[:3])
        if prefix == 500:
            img_path = f"{PATH_PREF_ITEM}/Pet/{item_id}.img/info/icon.png"
        elif 500 <= prefix < 600:
            img_path = f"{PATH_PREF_ITEM}/Cash/0{prefix}.img/0{item_id}/info/icon.png"
        elif prefix >= 900:
            img_path = f"{PATH_PREF_ITEM}/Special/0{prefix}.img/{item_id}/icon.png"
        else:
            print(f"Unknown file path for item ID: {item_id}")
            return

    if not os.path.isfile(dest_file):
        shutil.copy(img_path, dest_file)

def get_images(item_dict):
    for sn_id, info in item_dict.items():
        item_id = info.get('itemID')
        dest_file = f'../upcoming-sales-website/public/images/{item_id}.png'
        process_item(item_id, dest_file)
        
        # Packages are nested so we need to call get_images again
        if int(str(item_id)[:3]) >= 900:
            for package_id, items in info.get('packageContents', {}).items():
                get_images(items)