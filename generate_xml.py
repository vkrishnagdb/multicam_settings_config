import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_xml(csv_file, xml_file):
    # Create the root element of the XML tree
    root = ET.Element("dslr_remote_pro_multi")
    
    # Mapping configuration names to XML element names
    config_mapping = {
        'output directory': 'output_directory',
        'comment': 'comment',
        'subfolder': 'subfolder',
        'prefix': 'prefix',
        'iso': 'iso',
        'tv': 'tv',
        'av': 'av',
        'size_quality': 'size_quality',
        'exposure_compensation': 'exposure_compensation',
        'metering_mode': 'metering_mode',
        'drive_mode': 'drive_mode',
        'picture_style': 'picture_style',
        'white_balance': 'white_balance',
        'kelvin': 'kelvin',
        'mirror_lockup': 'mirror_lockup'
    }

    # Initialize camera settings
    camera_settings = {}

    # Read values from the CSV file and generate XML elements for configurations
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            config = row['config']
            value = row['value']
            
            # Check if the config value is one of the specified configurations
            if config.lower() in config_mapping:
                # If the configuration is ISO through mirror lockup, store it in camera_settings
                if config.lower() in ['iso', 'tv', 'av', 'size_quality', 'exposure_compensation', 
                                      'metering_mode', 'drive_mode', 'picture_style', 'white_balance',
                                      'kelvin', 'mirror_lockup']:
                    camera_settings[config_mapping[config.lower()]] = value
                else:
                    # Create XML element for each configuration
                    config_elem = ET.SubElement(root, config_mapping[config.lower()])
                    config_elem.text = value

    # Create XML element for comment
    comment_elem = root.find('comment')
    
    # Create XML element for camera settings under the camera element
    camera_elem = ET.SubElement(root, "camera", id="*", gang_settings="1")
    for setting, value in camera_settings.items():
        setting_elem = ET.SubElement(camera_elem, setting)
        setting_elem.text = value
    
    # Create and write the XML tree to file
    xml_string = prettify_xml(root)
    with open(xml_file, 'w') as f:
        f.write(xml_string)

# Example usage
csv_file = 'config_values.csv'
xml_file = 'settings.xml'
create_xml(csv_file, xml_file)
