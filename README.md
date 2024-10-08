# Application de Liste des Pokémon Combattants

## Description

Cette application simule un tournoi de Pokémons récupérés par consommation d'API avec une interface utilisateur stylisée utilisant PicoCSS et animations fournies par GSAP.

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
   http://127.0.0.1:5000