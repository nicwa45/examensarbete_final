import requests

# Constants for the Stratz API
STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STRATZ_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYmIwYjcwZGItMzNlYi00OGUzLThhYjUtNWNmZmEzYjhiMTc1IiwiU3RlYW1JZCI6IjI2ODY0ODM0IiwibmJmIjoxNzMzMTU1OTc5LCJleHAiOjE3NjQ2OTE5NzksImlhdCI6MTczMzE1NTk3OSwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.J4n-S_sHCAAwgz7MR_rNUIr61dfgLqZqZV_vA_R9qaI"  # Replace with your Stratz API token

def fetch_all_heroes():
    # GraphQL query to fetch all heroes and their abilities
    query = """
    {
      constants {
        heroes {
          id
          name
          abilities {
            slot
            ability {
              name
              language {
                displayName
                description
              }
              stat {
                cooldown
                manaCost
              }
            }
          }
        }
      }
    }
    """

    # Make the API request
    response = requests.post(
        STRATZ_GRAPHQL_URL,
        json={"query": query},
        headers={
            "Authorization": f"Bearer {STRATZ_AUTH_TOKEN}",
            "User-Agent": "STRATZ_API",
        },
    )

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        heroes = data.get("data", {}).get("constants", {}).get("heroes", [])
        return heroes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Fetch all heroes
heroes = fetch_all_heroes()

# Print hero and ability information
if heroes:
    for hero in heroes:
        print(f"Hero ID: {hero['id']}, Name: {hero['name']}")
        for ability in hero.get("abilities", []):
            if ability["ability"]["name"] != "generic_hidden":  # Exclude hidden abilities
                print(f"  Ability: {ability['ability']['language']['displayName']}")
                print(f"    Description: {ability['ability']['language']['description']}")
                print(f"    Cooldown: {', '.join(map(str, ability['ability']['stat']['cooldown'] or []))}")
                print(f"    Mana Cost: {', '.join(map(str, ability['ability']['stat']['manaCost'] or []))}")
        print("-" * 40)
else:
    print("Failed to fetch heroes.")

