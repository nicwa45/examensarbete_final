from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.opendota.com/api"
STRATZ_GRAPHQL_URL = "https://api.stratz.com/graphql"
STRATZ_AUTH_TOKEN = "" 


@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend


@app.route('/heroes', methods=['GET'])
def get_heroes():
    # Fetch all heroes to populate the dropdown
    response = requests.get(f"{API_BASE_URL}/heroStats")
    if response.status_code == 200:
        heroes = response.json()
        # Return only hero IDs and names for dropdown
        hero_list = [{"id": hero["id"], "localized_name": hero["localized_name"]} for hero in heroes]
        return jsonify(hero_list)
    else:
        return jsonify({"error": "Failed to fetch heroes"}), response.status_code


@app.route('/hero/<int:hero_id>', methods=['GET'])
def get_hero_stats(hero_id):
    # Fetch all hero stats from OpenDota API
    response = requests.get(f"{API_BASE_URL}/heroStats")
    if response.status_code == 200:
        hero_data = response.json()
        # Find the specific hero by ID
        hero_details = next((hero for hero in hero_data if hero["id"] == hero_id), None)
        if hero_details:
            # Fetch abilities from Stratz API
            abilities_response = fetch_hero_abilities(hero_id)
            if abilities_response:
                hero_details["abilities"] = abilities_response
            return jsonify(hero_details)
        else:
            return jsonify({"error": "Hero not found"}), 404
    else:
        return jsonify({"error": "Failed to fetch hero stats"}), response.status_code


@app.route('/hero/<int:hero_id>/abilities', methods=['GET'])
def get_hero_abilities_endpoint(hero_id):
    abilities = fetch_hero_abilities(hero_id)
    if abilities:
        return jsonify(abilities)
    return jsonify({"error": "Failed to fetch abilities"}), 500


def fetch_hero_abilities(hero_id):
    query = """
    {
      constants {
        hero(id: %d) {
          abilities {
            ability {
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
    """ % hero_id

    response = requests.post(
        STRATZ_GRAPHQL_URL,
        json={"query": query},
        headers={"Authorization": f"Bearer {STRATZ_AUTH_TOKEN}"}
    )

    if response.status_code == 200:
        data = response.json()
        hero_data = data.get("data", {}).get("constants", {}).get("hero", {})
        if hero_data:
            abilities = [
                {
                    "name": ability["ability"]["language"]["displayName"],
                    "description": ability["ability"]["language"]["description"],
                    "cooldown": ability["ability"]["stat"]["cooldown"] or [],
                    "manaCost": ability["ability"]["stat"]["manaCost"] or [],
                }
                for ability in hero_data.get("abilities", [])
                if ability["ability"]["language"]["displayName"]  # Exclude generic hidden abilities
            ]
            return abilities
    return None


if __name__ == '__main__':
    app.run(debug=True)
