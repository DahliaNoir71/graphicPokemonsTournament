# Application de Liste des Pokémon Combattants

## Description

Cette application affiche une liste des Pokémon combattants avec une interface utilisateur stylisée utilisant PicoCSS et animations fournies par GSAP. Elle permet également de démarrer un tournoi Pokémon à partir de la liste affichée.

## Fonctionnalités

- Affichage de la liste des Pokémon combattants avec leurs images.
- Utilisation de PicoCSS pour le design des éléments.
- Animations GSAP pour une apparence dynamique des cartes de Pokémon.
- Bouton pour démarrer un tournoi Pokémon.

## Prérequis

- Python 3.12.7
- Flask
- Jinja2
- Werkzeug
- click
- pip
- requests

## Installation

1. Clonez le dépôt de l'application :
    ```bash
    git clone <URL_DU_DEPOT>
    cd <NOM_DU_DEPOT>
    ```

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Pour Windows: venv\Scripts\activate
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

1. Lancez le serveur Flask :
    ```bash
    flask run
    ```

2. Ouvrez votre navigateur et accédez à l'adresse suivante :