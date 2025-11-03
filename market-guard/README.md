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



