import os
import resend
from dotenv import load_dotenv


load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")


def send_mail(subject: str, html: str):
	"""
	Envoie un email via Resend avec un sujet et un contenu HTML.
	Utilise MAIL_TO depuis .env pour le destinataire.
	"""
	to = os.getenv("MAIL_TO")
	if not resend.api_key or not to:
		raise ValueError("Clé Resend ou MAIL_TO manquant dans .env")

	return resend.Emails.send({
		"from": "MarketGuard <alerts@resend.dev>",
		"to": [to],
		"subject": subject,
		"html": html,
	})

