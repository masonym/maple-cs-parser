import xml.etree.ElementTree as ET
import shutil
import os
import os.path
import re
from utils import get_boto3_session

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Toggle to save images locally instead of uploading to S3
SAVE_IMAGES_LOCALLY = os.environ.get('SAVE_IMAGES_LOCALLY', '').lower() in ('1', 'true', 'yes', 'y')
# Base directory for local image saves
LOCAL_IMAGE_DIR = os.environ.get('LOCAL_IMAGE_DIR', 'local_images')

DUMPED_WZ = '../dumped_wz'
PATH_PREF_CHAR = f"../CharacterItems/"
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

s3 = None
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', "maplestory-items")
if not SAVE_IMAGES_LOCALLY:
    session = get_boto3_session()
    s3 = session.client('s3')

def get_xml_path(item_id):
    prefix = int(str(item_id)[:3])
    for key, path in PREFIX_PATH_MAP.items():
        if isinstance(key, range) and prefix in key or prefix == key:
            # Create a regex pattern for the folder name
            folder_pattern = re.compile(f"^{path}(?:\.wz)?(?:-\d+)?$")
            
            # Iterate over immediate subdirectories of PATH_PREF_CHAR
            for folder in os.listdir(PATH_PREF_CHAR):
                if folder_pattern.match(folder):
                    full_path = os.path.join(PATH_PREF_CHAR, folder, f"0{item_id}.img.xml").replace("\\","/")
                    if os.path.exists(full_path):
                        return full_path
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
    
    # Split the path into components
    path_components = outlink_value.split('/')
    
    # The first component is usually './SomeFolder'
    first_folder = path_components[1]
    # Create a regex pattern for the first folder
    folder_pattern = re.compile(f"^{first_folder}(?:\.wz)?(?:-\d+)?$")
    
    # Search for matching folder in DUMPED_WZ
    for folder in os.listdir(PATH_PREF_CHAR):
        if folder_pattern.match(folder):
            # Reconstruct the path with the matched folder
            reconstructed_path = os.path.join(PATH_PREF_CHAR, folder, *path_components[2:]).replace("\\","/")
            reconstructed_path += ".png"
            if os.path.exists(reconstructed_path):
                return reconstructed_path
    # print("None? ", outlink_value)
    return None

def upload_to_s3(local_file, s3_file):
    if SAVE_IMAGES_LOCALLY:
        dest_path = os.path.join(LOCAL_IMAGE_DIR, s3_file).replace("\\","/")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        try:
            shutil.copyfile(local_file, dest_path)
            print(f"Saved locally: {dest_path}")
            return True
        except FileNotFoundError:
            print(f"File not found: {local_file}")
            return False
        except Exception as e:
            print(f"Error saving locally: {e}")
            return False
    else:
        try:
            s3.upload_file(local_file, BUCKET_NAME, s3_file)
            print(f"Upload successful: {s3_file} to {BUCKET_NAME}")
            return True
        except FileNotFoundError:
            print(f"File not found: {local_file}")
            return False
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False

def process_item(item_id, s3_file):
    xml_path = get_xml_path(item_id)
    if xml_path and os.path.isfile(xml_path):
        img_path = get_image_path(xml_path)
        print(f"Item ID: {item_id} and Image Path: { img_path}")
    else:
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

        img_path = f"{base_path}/iconRaw.png"
        if not os.path.isfile(img_path):
            img_path = f"{base_path}/icon.png"
            if not os.path.isfile(img_path):
                print(f"No icon found for item ID: {item_id}")
                return

    if img_path is not None:
        print(img_path)
        upload_to_s3(img_path, s3_file)
    else:
        print("Path not found:", img_path)

def get_images(item_dict):
    for sn_id, info in item_dict.items():
        item_id = info.get('itemID')
        s3_file = f'images/{item_id}.png'
        process_item(item_id, s3_file)
        
        # Packages are nested so we need to call get_images again
        if int(str(item_id)[:3]) >= 900:
            for package_id, items in info.get('packageContents', {}).items():
                get_images(items)