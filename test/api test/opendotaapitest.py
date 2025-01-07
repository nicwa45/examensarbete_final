import requests

API_BASE_URL = "https://api.opendota.com/api"

response = requests.get(f"{API_BASE_URL}/heroStats")
if response.status_code == 200:
    heroes = response.json()
    for hero in heroes:
        print(f"Hero ID: {hero['id']}, Hero Name: {hero['localized_name']}")
else:
    print(f"Failed to fetch heroes: {response.status_code}")