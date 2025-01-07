from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.opendota.com/api"

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
    # Fetch all hero stats from the API
    response = requests.get(f"{API_BASE_URL}/heroStats")
    if response.status_code == 200:
        hero_data = response.json()
        # Find the specific hero by ID
        hero_details = next((hero for hero in hero_data if hero["id"] == hero_id), None)
        if hero_details:
            return jsonify(hero_details)
        else:
            return jsonify({"error": "Hero not found"}), 404
    else:
        return jsonify({"error": "Failed to fetch hero stats"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)