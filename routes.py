from flask import render_template
from services.pokemon_service import get_random_pokemons
from services.tournament_service import simulate_tournament

selected_pokemons = []

def register_routes(app):
    @app.route('/')
    def index():
        """
        Home page: Display randomly selected Pokémon participants.
        """
        global selected_pokemons
        selected_pokemons = get_random_pokemons()
        return render_template('participants.html', pokemons=selected_pokemons)

    @app.route('/tournament/<int:round_number>')
    def tournament(round_number):
        """
        Tournament page: Simulate battles round by round.
        """
        global selected_pokemons
        rounds, champion = simulate_tournament(selected_pokemons.copy())
        if round_number > len(rounds):
            return render_template('champion.html', champion=champion)
        current_round = rounds[round_number - 1]
        total_rounds = len(rounds)
        return render_template('tournament.html', round=current_round, round_number=round_number, total_rounds=total_rounds)
