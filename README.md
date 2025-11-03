botinvesty
===========

Un squelette minimal pour démarrer un bot d'investissement en Python.

Démarrage rapide
----------------

1. Créer un environnement virtuel et installer les dépendances:
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2. Créer un fichier `.env` (optionnel) à partir de l'exemple:
```bash
copy .env.example .env
```

3. Lancer le programme:
```bash
python -m bot_investy
```

Structure
---------
```
.
├─ bot_investy/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ config.py
│  └─ strategies/
│     ├─ __init__.py
│     └─ sample_strategy.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

Prochaines étapes
-----------------
- Implémenter une première stratégie simple (ex: buy & hold ou crossover MA)
- Ajouter un fournisseur de données (API ou CSV local)
- Connecter un broker (mock d'abord)
- Ajouter des tests et une CI simple


