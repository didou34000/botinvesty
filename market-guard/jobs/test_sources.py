import os
from app.sources import fetch_prices, fetch_macro, fetch_news_texts


if __name__ == "__main__":
	syms = os.getenv("WATCHLIST", "ACWI,QQQ,GLD").split(",")
	prices = fetch_prices(syms)
	macro = fetch_macro()
	news = fetch_news_texts()

	print("✅ Prix récupérés :", len(prices), "lignes pour", len(prices.columns), "actifs")
	print("✅ Données macro :", len(macro), "lignes")
	print("✅ Actualités :", len(news), "titres")


