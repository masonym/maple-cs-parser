import xml.etree.ElementTree as ET
import shutil
import os
import os.path

DUMPED_WZ = '../dumped_wz'
PATH_PREF_CHAR = f"{DUMPED_WZ}/Character.wz"
PATH_PREF_ITEM = f"{DUMPED_WZ}/Item.wz"

PREFIX_PATH_MAP = {
    range(2, 6): "Face",
    100: "Cap",
    range(101, 104): "Accessory",
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
    
    # Try to find iconRaw first, then fall back to icon
    icon_canvas = root.find(".//canvas[@name='iconRaw']")
    if icon_canvas is None:
        icon_canvas = root.find(".//canvas[@name='icon']")
    
    if icon_canvas is None:
        print(f"No icon or iconRaw found in {xml_path}")
        return None
    
    outlink_element = icon_canvas.find("string[@name='_outlink']")
    if outlink_element is None:
        print(f"No _outlink found in {xml_path}")
        return None
    
    outlink_value = outlink_element.attrib['value']
    modified_outlink_value = outlink_value.replace('Character/', 'Character.wz/')
    return f"{DUMPED_WZ}/{modified_outlink_value}.png"

def process_item(item_id, dest_file):
    xml_path = get_xml_path(item_id)
    if xml_path and os.path.isfile(xml_path):
        img_path = get_image_path(xml_path)
    else:
        # Pets, Cash Items, and Packages
        prefix = int(str(item_id)[:3])
        if prefix == 500:
            base_path = f"{PATH_PREF_ITEM}/Pet/{item_id}.img/info"
        elif 500 <= prefix < 600:
            base_path = f"{PATH_PREF_ITEM}/Cash/0{prefix}.img/0{item_id}/info"
        elif prefix >= 900:
            base_path = f"{PATH_PREF_ITEM}/Special/0{prefix}.img/{item_id}"
        else:
            print(f"Unknown file path for item ID: {item_id}")
            return

        # Try iconRaw.png first, then fallback to icon.png
        img_path = f"{base_path}/iconRaw.png"
        if not os.path.isfile(img_path):
            img_path = f"{base_path}/icon.png"
            if not os.path.isfile(img_path):
                print(f"No icon found for item ID: {item_id}")
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