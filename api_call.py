import requests
import xml.etree.ElementTree as ET
from datetime import datetime

'''

This is a script to parse the sales data using maplestory.io's api. 

While this works, maplestory.io often does not update hastily. 

'''


tree = ET.parse('qualifying_dirs.xml')
root = tree.getroot()

region = 'GMS'
version = '247'

for dir_element in root.findall('dir'):
    item_id = dir_element.find("int32[@name='ItemId']").get('value')
    term_start = dir_element.find("int32[@name='termStart']").get('value')
    term_start_f = datetime.strptime(term_start, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')
    term_end = dir_element.find("int32[@name='termEnd']").get('value')
    term_end_f = datetime.strptime(term_end, '%Y%m%d%H').strftime('%m-%d-%Y %H:00 UTC')

    response = requests.get(f'https://maplestory.io/api/{region}/{version}/item/{item_id}/name')
    
    if response.status_code == 200:
        item_name = response.json()['name']
        print(f"Item Name: {item_name}, Sale Duration: {term_start_f} - {term_end_f}")
    else:
        print(f"Failed to fetch item name for Item ID: {item_id}")
