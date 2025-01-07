// Fetch all heroes to populate the dropdown
function fetchHeroes() {
    fetch('/heroes')
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById('heroDropdown');
            dropdown.innerHTML = '<option value="">--Select--</option>'; // Default option
            data.forEach(hero => {
                const option = document.createElement('option');
                option.value = hero.id;
                option.textContent = hero.localized_name;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching hero list:', error));
}

// Fetch details for the selected hero
function fetchHeroDetails() {
    const heroId = document.getElementById('heroDropdown').value;

    if (!heroId) {
        document.getElementById('heroStats').innerHTML = '<p>Please select a hero to see details.</p>';
        return;
    }

    fetch(`/hero/${heroId}`)
        .then(response => response.json())
        .then(data => {
            const statsDiv = document.getElementById('heroStats');
            statsDiv.innerHTML = `
                <h2>${data.localized_name}</h2>
                <img src="https://api.opendota.com${data.icon}" alt="${data.localized_name}" style="width:50px; height:auto;">
                <p><strong>Primary Attribute:</strong> ${data.primary_attr}</p>
                <p><strong>Attack Type:</strong> ${data.attack_type}</p>
                <p><strong>Roles:</strong> ${data.roles.join(', ')}</p>
                <h3>Base Stats:</h3>
                <ul>
                    <li><strong>Base Health:</strong> ${data.base_health} (+${data.base_health_regen} regen)</li>
                    <li><strong>Base Mana:</strong> ${data.base_mana} (+${data.base_mana_regen} regen)</li>
                    <li><strong>Base Armor:</strong> ${data.base_armor}</li>
                    <li><strong>Base Attack Damage:</strong> ${data.base_attack_min} - ${data.base_attack_max}</li>
                    <li><strong>Base Strength:</strong> ${data.base_str} (+${data.str_gain})</li>
                    <li><strong>Base Agility:</strong> ${data.base_agi} (+${data.agi_gain})</li>
                    <li><strong>Base Intelligence:</strong> ${data.base_int} (+${data.int_gain})</li>
                    <li><strong>Attack Range:</strong> ${data.attack_range}</li>
                    <li><strong>Move Speed:</strong> ${data.move_speed}</li>
                    <li><strong>Day Vision:</strong> ${data.day_vision}</li>
                    <li><strong>Night Vision:</strong> ${data.night_vision}</li>
                </ul>
                <h3>Win Rate Stats:</h3>
                <ul>
                    <li><strong>Turbo:</strong> ${((data.turbo_wins / data.turbo_picks) * 100).toFixed(2)}% (${data.turbo_wins} wins / ${data.turbo_picks} picks)</li>
                    <li><strong>Herald:</strong> ${((data['1_win'] / data['1_pick']) * 100).toFixed(2)}% (${data['1_win']} wins / ${data['1_pick']} picks)</li>
                    <li><strong>Guardian:</strong> ${((data['2_win'] / data['2_pick']) * 100).toFixed(2)}% (${data['2_win']} wins / ${data['2_pick']} picks)</li>
                    <li><strong>Crusader:</strong> ${((data['3_win'] / data['3_pick']) * 100).toFixed(2)}% (${data['3_win']} wins / ${data['3_pick']} picks)</li>
                    <li><strong>Archon:</strong> ${((data['4_win'] / data['4_pick']) * 100).toFixed(2)}% (${data['4_win']} wins / ${data['4_pick']} picks)</li>
                    <li><strong>Legend:</strong> ${((data['5_win'] / data['5_pick']) * 100).toFixed(2)}% (${data['5_win']} wins / ${data['5_pick']} picks)</li>
                    <li><strong>Ancient:</strong> ${((data['6_win'] / data['6_pick']) * 100).toFixed(2)}% (${data['6_win']} wins / ${data['6_pick']} picks)</li>
                    <li><strong>Divine:</strong> ${((data['7_win'] / data['7_pick']) * 100).toFixed(2)}% (${data['7_win']} wins / ${data['7_pick']} picks)</li>
                    <li><strong>Immortal:</strong> ${((data['8_win'] / data['8_pick']) * 100).toFixed(2)}% (${data['8_win']} wins / ${data['8_pick']} picks)</li>
                </ul>
                <h3>Professional Stats:</h3>
                <ul>
                    <li><strong>Pro Bans:</strong> ${data.pro_ban}</li>
                    <li><strong>Pro Picks:</strong> ${data.pro_pick}</li>
                    <li><strong>Pro Wins:</strong> ${data.pro_win}</li>
                    <li><strong>Pro Win Rate:</strong> ${((data.pro_win / data.pro_pick) * 100).toFixed(2)}%</li>
                </ul>
            `;

            // Fetch abilities
            fetch(`/hero/${heroId}/abilities`)
                .then(response => response.json())
                .then(abilities => {
                    const abilitiesDiv = document.getElementById('abilities');
                    abilitiesDiv.innerHTML = '<h3>Abilities:</h3>';
                    abilities.forEach(ability => {
                        abilitiesDiv.innerHTML += `
                            <div>
                                <h4>${ability.name}</h4>
                                <p>${ability.description}</p>
                                <p><strong>Cooldown:</strong> ${ability.cooldown.join(', ')}</p>
                                <p><strong>Mana Cost:</strong> ${ability.manaCost.join(', ')}</p>
                            </div>
                        `;
                    });
                })
                .catch(error => {
                    console.error('Error fetching abilities:', error);
                    const abilitiesDiv = document.getElementById('abilities');
                    abilitiesDiv.innerHTML = '<p>No abilities found.</p>';
                });
        })
        .catch(error => {
            console.error('Error fetching hero stats:', error);
            document.getElementById('heroStats').innerHTML = '<p>Error fetching hero stats. Please try again later.</p>';
        });
}

// Automatically fetch heroes when the page loads
window.onload = fetchHeroes;