Étape 3 — .env
----------------

1) Copier l'exemple vers `.env` (ne pas committer `.env`):
```bash
copy .env.example .env   # Windows
# ou
cp .env.example .env     # macOS/Linux
```

2) Ouvrir `.env` et renseigner:
- `RESEND_API_KEY` (clé Resend, commence par `re_`)
- `MAIL_TO` (email de réception)

3) Vérifier la configuration:
```bash
python jobs/check_dotenv.py
```

Si tout est correct, le script affiche `DOTENV OK`.

Étape 4 — Test Email
---------------------

Lancer le test d'envoi d'email via Resend:
```bash
python jobs/send_test_mail.py
```

Si tu ne reçois pas l'email:
- Vérifie le dossier spam
- Assure-toi que `MAIL_TO` dans `.env` est correct
- Vérifie que `RESEND_API_KEY` commence par `re_`

Étape 5 — Test sources.py
-------------------------

Tester la collecte de données (prix, macro, actualités):
```bash
python jobs/test_sources.py
```

Étape 6 — Features
------------------

Tester les features calculées sur la première valeur de la watchlist:
```bash
python jobs/test_features.py
```

Étape 7 — Scoring
-----------------

Calculer et afficher le classement des actifs (0..100):
```bash
python jobs/test_scoring.py
```

Étape 7 — Sentiment (VADER)
---------------------------

Transformer des textes d’actualité en un score 0–100 (0 = pessimiste, 50 = neutre, 100 = euphorique):
```bash
python jobs/test_sentiment.py
```

Étape 8 — Scoring
-----------------

Scoring global avec trois sous-scores (poids 0.4/0.4/0.2):
- RiskOn (momentum 12m, distance MA200, vol20)
- Macro (CPI trend, PMI placeholder=50, pente courbe 2Y–10Y, chômage trend)
- News (sentiment RSS via VADER)

Exécuter:
```bash
python -m jobs.test_scoring
```
Note: le PMI est un placeholder (50) tant qu’aucune source fiable n’est branchée.

Étape 9 — Signaux
-----------------

Générer des signaux BUY/HOLD/SELL par actif avec une MA adaptative et une confiance 0–100:
```bash
python -m jobs.test_signals
```
Règles:
- BUY: prix au-dessus de la MA adaptive ET momentum 6m > 0
- SELL: prix sous la MA ET volatilité 20j > 1.2× sa médiane 1 an
- HOLD sinon

Étape 10 — Déclencheur
----------------------

Décider d'envoyer une alerte globale avec hystérésis, debounce et cooldown. État stocké dans `state/global.json`.
```bash
python -m jobs.test_trigger
```
Variables `.env`:
- `GLOBAL_HI`, `GLOBAL_LO`: seuils haut/bas
- `DEBOUNCE_RUNS`: nombre de passages consécutifs requis
- `COOLDOWN_GLOBAL_DAYS`: délai minimal entre deux emails globaux

Étape 11 — run_cycle
--------------------

Exécuter le pipeline et envoyer un email seulement si le déclencheur le décide:
```bash
# une passe
python -m jobs.run_cycle

# boucle 180 minutes
python -m jobs.run_cycle --loop 180
# ou via variable d'env
LOOP_MINUTES=180 python -m jobs.run_cycle
```
Rappel: l'email est envoyé uniquement si `maybe_alert_global` confirme (anti-spam).

Étape 11bis — IA Analyst
------------------------

Activer dans `.env`:
```
ENABLE_AI_ANALYST=true
OPENAI_API_KEY=sk_...
AI_MODEL=gpt-5
AI_MAX_TOKENS=600
```
Tester:
```bash
python -m jobs.test_analyst
```
Note: l'IA commente le contexte (verdict/rationale/points/risques) mais ne déclenche pas l'envoi; seul `maybe_alert_global` le fait.



