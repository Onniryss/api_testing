# API Testing

## Description

Ce projet a pour but de développer mes compétences en testing de client API.

## Structure

```txt
fakes/              # mocks custom
tests/              # Suite de tests
.env                # variables d'environnement
client.py           # Client API
connector.py        # Classe pour la connection et l'insertion dans la BD
exceptions.py       # Classes d'exceptions de l'API
protocols.py        # Interfaces
```

Le fichier .env contient ces variables d'environnement :

```py
API_URL = ""    # Base de l'url de requete
API_KEY = ""    # Token de l'API utilisée
```

## Tests

Pour lancer les tests de façon classique, utilisez simplement la commande `pytest`.
Pour voir la couverture de test, lancez la commande suivante :

```sh
pip install pytest-cov
pytest --cov-report=term-missing --cov=.
```