import xml.etree.ElementTree as ET

def load_xml_info():
    try:
        tree = ET.parse("client/data-client/info.xml")
        root = tree.getroot()
        bank = root.find("bank").text
        account = root.find("account").text
        receiver_name = root.find("receiver_name").text
        return bank, account, receiver_name
    except (FileNotFoundError, AttributeError):
        return "", "", ""

def save_xml_info(bank, account, receiver_name):
    try:
        root = ET.Element("info")
        bank_element = ET.SubElement(root, "bank")
        bank_element.text = bank
        account_element = ET.SubElement(root, "account")
        account_element.text = account
        receiver_name_element = ET.SubElement(root, "receiver_name")
        receiver_name_element.text = receiver_name
        tree = ET.ElementTree(root)
        tree.write("client/data-client/info.xml")
        return True
    except Exception as e:
        print(f"Error saving XML: {e}")
        return False