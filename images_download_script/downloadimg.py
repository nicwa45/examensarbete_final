import os
import requests

# Base URL for Dota 2 hero images
base_url = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/"

# Directory to save images locally
local_dir = "hero_images/"
os.makedirs(local_dir, exist_ok=True)

# JSON data containing hero information
heroes = [
    "antimage", "axe", "bane", "bloodseeker", "crystal_maiden",
    "drow_ranger", "earthshaker", "juggernaut", "mirana", "morphling",
    "nevermore", "phantom_lancer", "puck", "pudge", "razor",
    "sand_king", "storm_spirit", "sven", "tiny", "vengefulspirit",
    "windrunner", "zeus", "kunkka", "lina", "lion",
    "shadow_shaman", "slardar", "tidehunter", "witch_doctor", "lich",
    "riki", "enigma", "tinker", "sniper", "necrolyte",
    "warlock", "beastmaster", "queenofpain", "venomancer", "faceless_void",
    "skeleton_king", "death_prophet", "phantom_assassin", "pugna", "templar_assassin",
    "viper", "luna", "dragon_knight", "dazzle", "rattletrap",
    "leshrac", "furion", "life_stealer", "dark_seer", "clinkz",
    "omniknight", "enchantress", "huskar", "night_stalker", "broodmother",
    "bounty_hunter", "weaver", "jakiro", "batrider", "chen",
    "spectre", "ancient_apparition", "doom_bringer", "ursa", "spirit_breaker",
    "gyrocopter", "alchemist", "invoker", "silencer", "obsidian_destroyer",
    "lycan", "brewmaster", "shadow_demon", "lone_druid", "chaos_knight",
    "meepo", "treant", "ogre_magi", "undying", "rubick",
    "disruptor", "nyx_assassin", "naga_siren", "keeper_of_the_light", "wisp",
    "visage", "slark", "medusa", "troll_warlord", "centaur",
    "magnataur", "shredder", "bristleback", "tusk", "skywrath_mage",
    "abaddon", "elder_titan", "legion_commander", "techies", "ember_spirit",
    "earth_spirit", "abyssal_underlord", "terrorblade", "phoenix", "oracle",
    "winter_wyvern", "arc_warden", "monkey_king", "dark_willow", "pangolier",
    "grimstroke", "hoodwink", "void_spirit", "snapfire", "mars",
    "ringmaster", "dawnbreaker", "marci", "primal_beast", "muerta",
    "kez"
]


# Download images
for hero_name in heroes:
    image_url = f"{base_url}{hero_name}.png"
    print(f"Downloading {hero_name} from {image_url}")
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join(local_dir, f"{hero_name}.png"), "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {hero_name}")
    else:
        print(f"Failed to download: {hero_name}")


