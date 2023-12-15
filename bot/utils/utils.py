import requests


def get_local_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        print(f"Error: {e}")
        return None
