import os, pandas as pd
from app.sources import fetch_prices, fetch_macro, fetch_news_texts
from app.features import momentum_6m, distance_ma200, vol20
from app.sentiment import news_sentiment_score
from app.scoring import riskon_score, macrohealth_score, global_score


if __name__ == "__main__":
	syms = os.getenv("WATCHLIST","ACWI,QQQ,GLD").split(",")
	prices = fetch_prices(syms)
	assert not prices.empty, "Pas de prix — vérifie ta WATCHLIST et Internet."

	# Référence risk-on: ACWI si dispo sinon 1er symbole
	ref = "ACWI" if "ACWI" in prices.columns else prices.columns[0]
	close = prices[ref].dropna()

	# RiskOn
	mom12 = momentum_6m(close)
	dist  = distance_ma200(close)
	v20   = vol20(close)
	r = riskon_score(mom12, dist, v20)

	# Macro
	macro = fetch_macro()
	cpi_trend = macro["CPI"].pct_change(12).iloc[-1] if "CPI" in macro else 0.0
	pmi = 50.0  # placeholder (si tu ajoutes une vraie série PMI plus tard)
	curve = (macro["DGS10"].iloc[-1] - macro["DGS2"].iloc[-1]) if {"DGS10","DGS2"}.issubset(macro.columns) else 0.0
	un_trend = macro["UNEMP"].pct_change(12).iloc[-1] if "UNEMP" in macro else 0.0
	m = macrohealth_score(cpi_trend, pmi, curve, un_trend)

	# News
	texts = fetch_news_texts()
	n = news_sentiment_score(texts)

	# Global
	g = global_score(m, r, n, weights=(0.4,0.4,0.2))

	print(f"RiskOn: {r:.1f} | Macro: {m:.1f} | News: {n:.1f} | Global: {g:.1f}")

	# Sanity checks
	assert 0 <= r <= 100, "RiskOn hors bornes"
	assert 0 <= m <= 100, "Macro hors bornes"
	assert 0 <= n <= 100, "News hors bornes"
	assert 0 <= g <= 100, "Global hors bornes"

	# Cohérence simple: Global doit être entre min et max des sous-scores
	assert min(r,m,n) - 1e-6 <= g <= max(r,m,n) + 1e-6, "Global incohérent (hors enveloppe)"

	print("SCORING OK — intégration risk/macro/news")


