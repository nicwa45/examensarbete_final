import requests

STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STRATZ_AUTH_TOKEN = "" #token removed because github uppload

query = """
{
  constants {
    heroes {
      id
      name
    }
  }
}
"""

response = requests.post(
    STRATZ_GRAPHQL_URL,
    json={"query": query},
    headers={
        "Authorization": f"Bearer {STRATZ_AUTH_TOKEN}",
        "User-Agent": "STRATZ_API",
    }
)

if response.status_code == 200:
    data = response.json()
    heroes = data.get("data", {}).get("constants", {}).get("heroes", [])
    for hero in heroes:
        print(f"Hero ID: {hero['id']}, Hero Name: {hero['name']}")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")
