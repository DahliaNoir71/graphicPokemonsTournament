from flask import Flask, render_template
import random
import requests

app = Flask(__name__)

BASE_URL_API = "https://pokeapi.co/api/v2/"
URL_POKEMON_API_BASE = "%spokemon" % BASE_URL_API
NB_PARTICIPANTS = 16

# Récupérer un pokémon aléatoire
def get_random_pokemon_id(pokemons_count):
    """
    :param pokemons_count: The total number of available Pokémon, used as the upper bound for generating a random Pokémon ID.
    :return: A random Pokémon ID within the range of 1 and the given number of Pokémons.
    """
    return random.randint(1, pokemons_count)

# Récupérer les données d'un pokémon
def fetch_pokemon_data(pokemon_id):
    """
    :param pokemon_id: ID of the Pokémon to fetch data for
    :return: JSON response containing Pokémon data if successful, None otherwise
    """
    try:
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        response = requests.get(url_pokemon)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Erreur lors de la récupération du Pokémon avec l'ID : {pokemon_id}")
        return None

# Obtenir une liste de pokémons aléatoires
def get_random_pokemons():
    """
    Fetches a list of random Pokémon data from the Pokémon API.

    The function makes a request to the Pokémon API to retrieve the total count of Pokémon resources.
    It then selects random Pokémon IDs and fetches their data until it accumulates the desired number
    of unique Pokémon.

    :return: A list of dictionaries containing Pokémon data.
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

# Calculer la force d'un pokémon
def calculate_pokemon_strength(pokemon):
    """
    :param pokemon: A dictionary containing details of a Pokemon, including its stats.
    :type pokemon: dict
    :return: The total strength of the Pokemon, calculated as the sum of its base stats.
    :rtype: int
    """
    stats = pokemon['stats']
    total_strength = sum(stat['base_stat'] for stat in stats)
    return total_strength

# Simuler un combat et déterminer le vainqueur
def simulate_battle(pokemon1, pokemon2):
    """
    :param pokemon1: The first Pokémon involved in the battle simulation.
    :param pokemon2: The second Pokémon involved in the battle simulation.
    :return: The winning Pokémon based on their calculated strengths. If both have the same strength, a random Pokémon is chosen as the winner.
    """
    strength1 = calculate_pokemon_strength(pokemon1)
    strength2 = calculate_pokemon_strength(pokemon2)

    if strength1 > strength2:
        return pokemon1
    elif strength2 > strength1:
        return pokemon2
    else:
        return random.choice([pokemon1, pokemon2])

# Route principale : Affichage du tournoi
@app.route('/')
def index():
    """
    Handles the root URL and renders the index page.

    :return: Rendered HTML of the index page.
    """
    return render_template('index.html')

# Route pour démarrer le tournoi
@app.route('/tournament')
def tournament():
    """
    Handles the tournament route which simulates a Pokémon tournament with randomly selected Pokémon.

    :return: A rendered HTML template for the tournament, showing all rounds and the champion.
    """
    pokemons = get_random_pokemons()  # Obtenons les Pokémon aléatoires
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
