// Fetch all heroes to populate the dropdown
function fetchHeroes() {
    fetch('/heroes')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const dropdown = document.getElementById('heroDropdown');
            dropdown.innerHTML = '<option value="">--Select--</option>'; // Default option

            if (data && data.length > 0) {
                data.forEach(hero => {
                    
                    const option = document.createElement('option');
                    option.value = hero.id;
            
                    // Add hero name to the dropdown
                    option.textContent = hero.localized_name;

                    dropdown.appendChild(option);
                });
            } else {
                console.error('No heroes found in API response.');
                dropdown.innerHTML = '<option value="">No heroes available</option>';
            }
        })
        .catch(error => {
            console.error('Error fetching hero list:', error);
            const dropdown = document.getElementById('heroDropdown');
            dropdown.innerHTML = '<option value="">Failed to load heroes</option>';
        });
}

// Fetch details for the selected hero
function fetchHeroDetails() {
    const heroId = document.getElementById('heroDropdown').value;

    if (!heroId) {
        document.getElementById('heroStats').innerHTML = '<p>Please select a hero to see details.</p>';
        document.getElementById('abilities').innerHTML = '<p>No abilities available.</p>';
        document.getElementById('winRateStats').innerHTML = '<p>No win rate stats available.</p>';
        document.getElementById('professionalStats').innerHTML = '<p>No professional stats available.</p>';
        return;
    }

    // Fetch hero stats (including abilities)
    fetch(`/hero/${heroId}`)
        .then(response => response.json())
        .then(data => {
            const statsDiv = document.getElementById('heroStats');
            const abilitiesDiv = document.getElementById('abilities');
            const winRateDiv = document.getElementById('winRateStats');
            const professionalDiv = document.getElementById('professionalStats');

            // Display hero  with Azure image
            statsDiv.innerHTML = `
                <h2>${data.localized_name}</h2>
                <img src="https://dota2heroimg.blob.core.windows.net/heroimg/hero_images/${data.localized_name.replace(/ /g, '_').toLowerCase()}.png" alt="${data.localized_name}" class="hero-image">
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
            `;

            // Display abilities
            if (data.abilities && data.abilities.length > 0) {
                abilitiesDiv.innerHTML = `<h3>Abilities:</h3>`;
                data.abilities.forEach(ability => {
                    abilitiesDiv.innerHTML += `
                        <div class="ability">
                            <img src="${ability.image_url}" alt="${ability.name}" class="ability-image">
                            <h4>${ability.name}</h4>
                            <p>${ability.description}</p>
                            <p><strong>Cooldown:</strong> ${ability.cooldown || 'N/A'}</p>
                            <p><strong>Mana Cost:</strong> ${ability.manaCost || 'N/A'}</p>
                        </div>
                    `;
                });
            } else {
                abilitiesDiv.innerHTML = `<p>No abilities available for this hero.</p>`;
            }


            // Display win rate stats
            winRateDiv.innerHTML = `
            <h3>Win and Pick Rate</h3>
            <ul>
                <li><strong>Turbo:</strong> ${calculateWinRate(data.turbo_wins, data.turbo_picks)}</li>
                <li><strong>Herald:</strong> ${calculateWinRate(data['1_win'], data['1_pick'])}</li>
                <li><strong>Guardian:</strong> ${calculateWinRate(data['2_win'], data['2_pick'])}</li>
                <li><strong>Crusader:</strong> ${calculateWinRate(data['3_win'], data['3_pick'])}</li>
                <li><strong>Archon:</strong> ${calculateWinRate(data['4_win'], data['4_pick'])}</li>
                <li><strong>Legend:</strong> ${calculateWinRate(data['5_win'], data['5_pick'])}</li>
                <li><strong>Ancient:</strong> ${calculateWinRate(data['6_win'], data['6_pick'])}</li>
                <li><strong>Divine:</strong> ${calculateWinRate(data['7_win'], data['7_pick'])}</li>
                <li><strong>Immortal:</strong> ${calculateWinRate(data['8_win'], data['8_pick'])}</li>
            </ul>
        `;
        


            // Display professional stats
            professionalDiv.innerHTML = `
                <ul>
                    <li><strong>Pro Bans:</strong> ${data.pro_ban}</li>
                    <li><strong>Pro Picks:</strong> ${data.pro_pick}</li>
                    <li><strong>Pro Wins:</strong> ${data.pro_win}</li>
                    <li><strong>Pro Win Rate:</strong> ${calculateWinRate(data.pro_win, data.pro_pick)}</li>
                </ul>
            `;
        })
        .catch(error => {
            console.error('Error fetching hero stats:', error);
            document.getElementById('heroStats').innerHTML = `<p>Error fetching hero stats. Please try again later.</p>`;
            document.getElementById('abilities').innerHTML = `<p>Failed to load abilities.</p>`;
            document.getElementById('winRateStats').innerHTML = `<p>Failed to load win rate stats.</p>`;
            document.getElementById('professionalStats').innerHTML = `<p>Failed to load professional stats.</p>`;
        });
}

// Helper function to calculate win rate
function calculateWinRate(wins, picks) {
    if (picks && picks > 0) {
        return `${((wins / picks) * 100).toFixed(2)}% (${wins} wins / ${picks} picks)`;
    }
    return "N/A";
}

// Automatically fetch heroes when the page loads
window.onload = fetchHeroes;

















