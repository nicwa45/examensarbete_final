import requests

STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STRATZ_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYmIwYjcwZGItMzNlYi00OGUzLThhYjUtNWNmZmEzYjhiMTc1IiwiU3RlYW1JZCI6IjI2ODY0ODM0IiwibmJmIjoxNzMzMTU1OTc5LCJleHAiOjE3NjQ2OTE5NzksImlhdCI6MTczMzE1NTk3OSwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.J4n-S_sHCAAwgz7MR_rNUIr61dfgLqZqZV_vA_R9qaI"

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