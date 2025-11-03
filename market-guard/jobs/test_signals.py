import os
from app.sources import fetch_prices
from app.signals import batch_signals


if __name__ == "__main__":
	syms = os.getenv("WATCHLIST","ACWI,QQQ,GLD,BTC-USD").split(",")
	prices = fetch_prices(syms)
	assert not prices.empty, "Pas de prix — vérifie WATCHLIST et Internet."

	df = batch_signals(prices)
	print(df.head(10).to_string(index=False))

	# Vérifs simples
	assert set(df["Signal"]).issubset({"BUY","HOLD","SELL"}), "Signal inconnu"
	assert df["Confidence"].between(0,100).all(), "Confiance hors bornes"
	assert df["ma_w"].between(60,250).all(), "Fenêtre MA hors bornes"
	assert df.shape[0] == len(syms), "Une colonne par ticker attendue"

	print("SIGNALS OK — génération BUY/HOLD/SELL et métriques")


