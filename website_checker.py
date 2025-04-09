import requests

def check_website(url):
    try:
        response = requests.get(url)
        if "Auto Bank Ver 1.0.0.0" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False