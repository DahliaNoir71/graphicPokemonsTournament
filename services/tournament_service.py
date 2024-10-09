import random


def calculate_pokemon_strength(pokemon):
    """
    :param pokemon: A dictionary representing a Pokémon, containing various stats.
    :return: The total strength of the Pokémon calculated by summing up its base stats.
    """
    return sum(stat['base_stat'] for stat in pokemon['stats'])


def simulate_battle(pokemon1, pokemon2):
    """
    Simulate a battle between two Pokémon.
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
    Simulate the tournament with all Pokémon participants.
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
                'winner': winner['name'],
            })

        rounds.append({
            'round_number': round_num,
            'battles': round_battles
        })

        pokemons = winners
        round_num += 1

    return rounds, pokemons[0]
