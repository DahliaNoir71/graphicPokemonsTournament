from flask import Flask, render_template
import random
import requests

app = Flask(__name__)

BASE_URL_API = "https://pokeapi.co/api/v2/"
URL_POKEMON_API_BASE = "%spokemon" % BASE_URL_API
NB_PARTICIPANTS = 16

participants = []

def get_random_pokemon_id(pokemons_count):
    """
    :param pokemons_count: Integer representing the total number of possible Pokémon.
    :return: Integer representing a randomly selected Pokémon ID.
    """
    return random.randint(1, pokemons_count)

def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: The ID of the Pokémon to retrieve data for.
    :return: A dictionary containing the Pokémon data if the request is successful, or None if an error occurs.
    """
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Erreur lors de la récupération du Pokémon avec l'ID : {pokemon_id}")
        return None

def get_random_pokemons():
    """
    Fetches a list of random pokemons.

    :return: A list of dictionaries, where each dictionary contains data about a random pokemon.
    """
    pokemons = []
    response = requests.get(URL_POKEMON_API_BASE)
    pokemons_count = response.json()["count"]

    while len(pokemons) < NB_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(pokemons_count)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons

def calculate_pokemon_strength(pokemon):
    """
    :param pokemon: A dictionary containing information about a Pokémon, including its stats
    :type pokemon: dict
    :return: The total strength of the Pokémon calculated by summing its base stats
    :rtype: int
    """
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength

def simulate_battle(pokemon1, pokemon2):
    """
    :param pokemon1: The first Pokemon involved in the battle.
    :param pokemon2: The second Pokemon involved in the battle.
    :return: The Pokemon that wins the battle, chosen randomly in case of a tie.
    """
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    if strength1 > strength2:
        return pokemon1
    elif strength2 > strength1:
        return pokemon2
    else:
        return random.choice([pokemon1, pokemon2])

@app.route('/')
def index():
    """
    Handles the root URL of the application.

    This route is responsible for initializing a global list of participants
    by fetching random Pokémon data. It then renders the `index.html` template,
    passing in the number of participants and the list of Pokémon.

    :return: Rendered HTML for the index page.
    """
    global participants
    participants = get_random_pokemons()
    return render_template('index.html', nbParticipants=NB_PARTICIPANTS, pokemons=participants)

@app.route('/tournament')
def tournament():
    """
    Handles the tournament route, simulating a series of battles between Pokémon participants until a champion is determined.

    :return: Renders the tournament results page with details of each round and the final champion.
    """
    global participants
    pokemons = participants
    rounds = []
    round_number = 1

    while len(pokemons) > 1:
        round_battles = []
        winners = []

        for i in range(0, len(pokemons), 2):
            pokemon1 = pokemons[i]
            pokemon2 = pokemons[i + 1]
            winner = simulate_battle(pokemon1, pokemon2)
            winners.append(winner)

            # Ajout des détails du combat (Pokémon 1, Pokémon 2, Vainqueur)
            round_battles.append({
                'pokemon1': pokemon1['name'],
                'pokemon1_img': pokemon1['sprites']['front_default'],
                'pokemon2': pokemon2['name'],
                'pokemon2_img': pokemon2['sprites']['front_default'],
                'winner': winner['name']
            })

        rounds.append({
            'round_number': round_number,
            'battles': round_battles
        })

        pokemons = winners
        round_number += 1

    # Le dernier Pokémon restant est le champion
    champion = pokemons[0]

    return render_template('tournament.html', rounds=rounds, champion=champion)

if __name__ == '__main__':
    app.run(debug=True)
