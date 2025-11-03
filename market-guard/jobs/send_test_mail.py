from app.emailer import send_mail


if __name__ == "__main__":
	subject = "Test MarketGuard ✅"
	body = "<h2>Bonjour 👋</h2><p>Ceci est un test d'envoi via Resend.</p>"
	send_mail(subject, body)
	print("✅ Mail envoyé (vérifie ta boîte).")


