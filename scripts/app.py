from flask import Flask, render_template
import random
import requests

app = Flask(__name__)

BASE_URL_API = "https://pokeapi.co/api/v2/"
URL_POKEMON_API_BASE = f"{BASE_URL_API}pokemon"
PARTICIPANTS_COUNT = 2

participants = []
round_number = 1


class PokemonManager:
    """Class to manage Pokémon data retrieval and battle simulation."""

    @staticmethod
    def get_random_pokemon_id(total_pokemons):
        """
        Return a randomly selected Pokémon ID.
        """
        return random.randint(1, total_pokemons)

    @staticmethod
    def fetch_pokemon_data(pokemon_id):
        """
        Retrieve data for the Pokémon with the given ID.
        """
        url_pokemon = f"{URL_POKEMON_API_BASE}/{pokemon_id}"
        try:
            response = requests.get(url_pokemon)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            print(f"Erreur lors de la récupération du Pokémon avec l'ID : {pokemon_id}")
            return None

    @staticmethod
    def get_random_pokemons():
        """
        Fetches a list of random Pokémon data.
        """
        pokemons = []
        response = requests.get(URL_POKEMON_API_BASE)
        total_pokemons = response.json()["count"]

        while len(pokemons) < PARTICIPANTS_COUNT:
            pokemon_id = PokemonManager.get_random_pokemon_id(total_pokemons)
            pokemon_data = PokemonManager.fetch_pokemon_data(pokemon_id)
            if pokemon_data and pokemon_data not in pokemons:
                pokemons.append(pokemon_data)

        return pokemons

    @staticmethod
    def calculate_pokemon_strength(pokemon):
        """
        Calculate total strength of a Pokémon.
        """
        return sum(stat['base_stat'] for stat in pokemon['stats'])

    @staticmethod
    def simulate_battle(pokemon1, pokemon2):
        """
        Simulate a battle between two Pokémon.
        """
        strength1 = PokemonManager.calculate_pokemon_strength(pokemon1)
        strength2 = PokemonManager.calculate_pokemon_strength(pokemon2)

        return random.choice([pokemon1, pokemon2]) if strength1 == strength2 else (
            pokemon1 if strength1 > strength2 else pokemon2)


@app.route('/')
def index():
    """
    Handles the root URL of the application.
    """
    global participants

    participants = PokemonManager.get_random_pokemons()
    return render_template('index.html', nbParticipants=PARTICIPANTS_COUNT, pokemons=participants)


@app.route('/tournament')
def tournament():
    """
    Simulates a series of battles until a Pokémon champion is determined.
    """
    global participants

    rounds = []
    round_number = 1

    while len(participants) > 1:
        round_battles = []
        winners = []

        for i in range(0, len(participants), 2):
            pokemon1 = participants[i]
            pokemon2 = participants[i + 1]
            winner = PokemonManager.simulate_battle(pokemon1, pokemon2)
            winners.append(winner)
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

        participants = winners
        round_number += 1

    champion = participants[0]
    return render_template('tournament.html', rounds=rounds, champion=champion)


if __name__ == '__main__':
    app.run(debug=True)
