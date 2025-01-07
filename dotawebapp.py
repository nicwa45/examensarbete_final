from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# API Base URLs and Authentication
API_BASE_URL = "https://api.opendota.com/api"
STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STRATZ_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYmIwYjcwZGItMzNlYi00OGUzLThhYjUtNWNmZmEzYjhiMTc1IiwiU3RlYW1JZCI6IjI2ODY0ODM0IiwibmJmIjoxNzMzMTU1OTc5LCJleHAiOjE3NjQ2OTE5NzksImlhdCI6MTczMzE1NTk3OSwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.J4n-S_sHCAAwgz7MR_rNUIr61dfgLqZqZV_vA_R9qaI"  # Replace with your Stratz API token

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend

@app.route('/heroes', methods=['GET'])
def get_heroes():
    # Fetch all heroes to populate the dropdown
    response = requests.get(f"{API_BASE_URL}/heroStats")
    if response.status_code == 200:
        heroes = response.json()
        # Return hero IDs, names, and image URLs for the dropdown
        hero_list = [
            {
                "id": hero["id"],
                "localized_name": hero["localized_name"],
                "image_url": f"https://dota2heroimg.blob.core.windows.net/heroimg/hero_images/{hero['localized_name'].lower().replace(' ', '_')}.png"
            }
            for hero in heroes
        ]
        return jsonify(hero_list)
    else:
        return jsonify({"error": "Failed to fetch heroes"}), response.status_code


@app.route('/hero/<int:hero_id>', methods=['GET'])
def get_hero_details(hero_id):
    response = requests.get(f"{API_BASE_URL}/heroStats")
    if response.status_code == 200:
        hero_data = response.json()
        hero_details = next((hero for hero in hero_data if hero["id"] == hero_id), None)

        if hero_details:
            # Fetch abilities
            abilities = fetch_hero_abilities(hero_id)
            if abilities:
                hero_details["abilities"] = abilities

            # Add Azure Blob Storage URL for the hero image
            hero_name = hero_details["localized_name"].lower().replace(" ", "_").replace("'", "")
            hero_details["image_url"] = f"https://dota2heroimg.blob.core.windows.net/heroimg/hero_images/{hero_name}.png"

            # Fetch abilities from Stratz API
            abilities = fetch_hero_abilities(hero_id)
            if abilities:
                hero_details["abilities"] = abilities

            # Add win rate brackets
            win_rate_brackets = {
                "Herald": get_win_rate(hero_details, "1"),
                "Guardian": get_win_rate(hero_details, "2"),
                "Crusader": get_win_rate(hero_details, "3"),
                "Archon": get_win_rate(hero_details, "4"),
                "Legend": get_win_rate(hero_details, "5"),
                "Ancient": get_win_rate(hero_details, "6"),
                "Divine": get_win_rate(hero_details, "7"),
                "Immortal": get_win_rate(hero_details, "8"),
            }
            hero_details["win_rate_brackets"] = win_rate_brackets

            # Add professional stats
            professional_stats = {
                "Pro Picks": hero_details.get("pro_pick", "N/A"),
                "Pro Wins": hero_details.get("pro_win", "N/A"),
                "Pro Bans": hero_details.get("pro_ban", "N/A"),
                "Pro Win Rate": f"{(hero_details['pro_win'] / hero_details['pro_pick'] * 100):.2f}%" if hero_details.get("pro_pick") else "N/A",
            }
            hero_details["professional_stats"] = professional_stats

            # Include vision stats
            hero_details["day_vision"] = hero_details.get("day_vision", "N/A")
            hero_details["night_vision"] = hero_details.get("night_vision", "N/A")

            return jsonify(hero_details)

        return jsonify({"error": "Hero not found"}), 404
    else:
        return jsonify({"error": "Failed to fetch hero stats"}), response.status_code


def fetch_hero_abilities(hero_id):
    query = """
    {
      constants {
        heroes {
          id
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
    response = requests.post(
        STRATZ_GRAPHQL_URL,
        json={"query": query},
        headers={
            "Authorization": f"Bearer {STRATZ_AUTH_TOKEN}",
            "User-Agent": "STRATZ_API",
        },
    )

    if response.status_code == 200:
        data = response.json()
        # Find abilities for the specific hero
        heroes = data.get("data", {}).get("constants", {}).get("heroes", [])
        hero = next((h for h in heroes if h["id"] == hero_id), None)
        if hero:
            return [
                {
                    "name": ability["ability"]["language"]["displayName"],
                    "description": ability["ability"]["language"]["description"],
                    "cooldown": " / ".join(map(str, ability["ability"].get("stat", {}).get("cooldown", []) or [])),
                    "manaCost": " / ".join(map(str, ability["ability"].get("stat", {}).get("manaCost", []) or [])),
                    "image_url": f"https://dota2heroimg.blob.core.windows.net/heroimg/ability_images/{ability['ability']['name']}.png",
                }
                for ability in hero["abilities"]
                if ability["ability"]["name"] != "generic_hidden"  # Exclude hidden abilities
            ]
    return None




def get_win_rate(hero_details, bracket):
    if hero_details.get(f"{bracket}_pick"):
        return f"{(hero_details[f'{bracket}_win'] / hero_details[f'{bracket}_pick'] * 100):.2f}% ({hero_details[f'{bracket}_win']} wins / {hero_details[f'{bracket}_pick']} picks)"
    return "N/A"

if __name__ == '__main__':
    app.run(debug=True)









