from flask import Flask, render_template, request, redirect, url_for
import random
import requests

app = Flask(__name__)

# Constants
BASE_API_URL = "https://pokeapi.co/api/v2/"
POKEMON_API_URL = f"{BASE_API_URL}pokemon"
NUM_PARTICIPANTS = 16

selected_pokemons = []


def get_random_pokemon_id(total_pokemons):
    """
    :param total_pokemons: The total number of Pokémon available.
    :return: A random Pokémon ID between 1 and the total number of Pokémon.
    """
    return random.randint(1, total_pokemons)


def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: The ID of the Pokémon to retrieve data for.
    :return: A dictionary containing Pokémon data if the request is successful, None otherwise.
    """
    url = f"{POKEMON_API_URL}/{pokemon_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Error retrieving Pokémon with ID : {pokemon_id}")
        return None


def get_random_pokemons():
    """
    Fetch a list of random Pokémon data.

    :return: A list of dictionaries, each containing data for a unique Pokémon.
    """
    pokemons = []
    response = requests.get(POKEMON_API_URL)
    total_pokemons = response.json()["count"]
    while len(pokemons) < NUM_PARTICIPANTS:
        pokemon_id = get_random_pokemon_id(total_pokemons)
        pokemon_data = fetch_pokemon_data(pokemon_id)
        if pokemon_data and pokemon_data not in pokemons:
            pokemons.append(pokemon_data)
    return pokemons


def calculate_pokemon_strength(pokemon):
    """
    :param pokemon: A dictionary representing a Pokémon, containing various stats.
    :return: The total strength of the Pokémon calculated by summing up its base stats.
    """
    return sum(stat['base_stat'] for stat in pokemon['stats'])


def simulate_battle(pokemon1, pokemon2):
    """
    :param pokemon1: The first Pokémon participating in the battle.
    :param pokemon2: The second Pokémon participating in the battle.
    :return: The winning Pokémon after the simulation.
    """
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)
    if strength1 > strength2:
        return pokemon1
    if strength2 > strength1:
        return pokemon2
    return random.choice([pokemon1, pokemon2])


def simulate_tournament(pokemons):
    """
    :param pokemons: A list of dictionaries, each representing a Pokémon with its attributes such as name and sprites.
    :return: A tuple containing:
        - rounds: A list of dictionaries, each representing a round with its battles.
        - The final winning Pokémon as a dictionary.
    """
    rounds = []
    round_num = 1
    while len(pokemons) > 1:
        round_battles = []
        winners = []
        for i in range(0, len(pokemons), 2):
            pokemon1 = pokemons[i]
            pokemon2 = pokemons[i + 1]
            winner = simulate_battle(pokemon1, pokemon2)
            winners.append(winner)
            round_battles.append({
                'pokemon1': pokemon1['name'],
                'pokemon1_img': pokemon1['sprites']['front_default'],
                'pokemon2': pokemon2['name'],
                'pokemon2_img': pokemon2['sprites']['front_default'],
                'winner': winner['name']
            })
        rounds.append({
            'round_number': round_num,
            'battles': round_battles
        })
        pokemons = winners
        round_num += 1
    return rounds, pokemons[0]


@app.route('/')
def index():
    """
    Route for the home page.

    This function handles the root URL endpoint ('/') and performs the following actions:
    1. Sets the `selected_pokemons` global variable with a list of random Pokemon objects by calling the `get_random_pokemons` function.
    2. Renders the 'participants.html' template, passing the list of selected Pokemon objects to it.

    :return: Rendered HTML page for the participants.html template with the selected Pokemon
    """
    global selected_pokemons
    selected_pokemons = get_random_pokemons()
    return render_template('participants.html', pokemons=selected_pokemons)


@app.route('/tournament/<int:round_number>')
def tournament(round_number):
    """
    :param round_number: The current round number of the tournament being accessed.
    :return: A rendered HTML template for the specified tournament round. If the round exceeds the total number of rounds, returns the champion page.
    """
    global selected_pokemons
    rounds, champion = simulate_tournament(selected_pokemons.copy())
    if round_number > len(rounds):
        return render_template('champion.html', champion=champion)
    current_round = rounds[round_number - 1]
    total_rounds = len(rounds)
    return render_template('tournament.html', round=current_round, round_number=round_number, total_rounds=total_rounds)


if __name__ == '__main__':
    app.run(debug=True)
