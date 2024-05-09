import xml.etree.ElementTree as ET
import shutil
import os
import os.path

DUMPED_WZ = '../dumped_wz'
PATH_PREF_CHAR = f"{DUMPED_WZ}/Character"
PATH_PREF_ITEM = f"{DUMPED_WZ}/Item.wz"

def get_images(item_dict):
    for sn_id, info in item_dict.items():
        item_id = info.get('itemID')
        prefix = int(str(info.get('itemID'))[:3])

        if prefix in range(2, 6):
            img_path = f"{PATH_PREF_CHAR}/Face/_Canvas/{item_id}.img/info/icon.png"
        elif prefix == 100:
            img_path = f"{PATH_PREF_CHAR}/Cap/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix in [101, 102, 103] or prefix in range(112, 120):
            img_path = f"{PATH_PREF_CHAR}/Accessory/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 104:
            img_path = f"{PATH_PREF_CHAR}/Coat/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 105:
            img_path = f"{PATH_PREF_CHAR}/Longcoat/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 106:
            img_path = f"{PATH_PREF_CHAR}/Pants/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 107:
            img_path = f"{PATH_PREF_CHAR}/Shoes/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 108:
            img_path = f"{PATH_PREF_CHAR}/Glove/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 109:
            img_path = f"{PATH_PREF_CHAR}/Shield/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 110:
            img_path = f"{PATH_PREF_CHAR}/Cape/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 111:
            img_path = f"{PATH_PREF_CHAR}/Ring/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 180:
            img_path = f"{PATH_PREF_CHAR}/PetEquip/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix in range(121, 172):
            xml_path = f"{PATH_PREF_CHAR}/Weapon/0{item_id}.img.xml"
            wep_tree = ET.parse(xml_path)
            root = wep_tree.getroot()
            icon_canvas = root.find(".//canvas[@name='icon']")
            outlink_value = icon_canvas.find("string[@name='_outlink']").attrib['value']
            img_path = f"{DUMPED_WZ}/{outlink_value}.png"
        elif prefix in [166, 167]:
            img_path = f"{PATH_PREF_CHAR}/Android/_Canvas/0{item_id}.img/info/icon.png"
        elif prefix == 500:
            img_path = f"{PATH_PREF_ITEM}/Pet/{item_id}.img/info/icon.png"
        elif prefix in range(500, 600):
            img_path = f"{PATH_PREF_ITEM}/Cash/0{prefix}.img/0{item_id}/info/icon.png"
        elif prefix >= 900:
            img_path = f"{PATH_PREF_ITEM}/Special/0{prefix}.img/{item_id}/icon.png"
            for package_id, items in info.get('packageContents', {}).items():
                get_images(items)
        else:
            img_path = f"Unknown file path for item ID: {item_id}"

        dest_file = f'../upcoming-sales-website/public/images/{item_id}.png'
        if not os.path.isfile(dest_file):
            shutil.copy(img_path, dest_file)