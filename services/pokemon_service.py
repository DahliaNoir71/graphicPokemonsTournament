import random
import requests

BASE_API_URL = "https://pokeapi.co/api/v2/"
POKEMON_API_URL = f"{BASE_API_URL}pokemon"
NUM_PARTICIPANTS = 16


def get_random_pokemon_id(total_pokemons):
    """
    :param total_pokemons: The total number of Pokémon available.
    :return: A random Pokémon ID between 1 and the total number of Pokémon.
    """
    return random.randint(1, total_pokemons)


def fetch_pokemon_data(pokemon_id):
    """
    Fetch Pokémon data by ID from the PokeAPI.
    """
    url = f"{POKEMON_API_URL}/{pokemon_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print(f"Error retrieving Pokémon with ID: {pokemon_id}")
        return None


def get_random_pokemons():
    """
    Fetch a list of random Pokémon data.
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

