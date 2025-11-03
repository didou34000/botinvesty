import os, pandas as pd
from app.sources import fetch_prices
from app.features import momentum_6m, distance_ma200, vol20, zscore, ma


if __name__ == "__main__":
	syms = os.getenv("WATCHLIST", "ACWI,QQQ,GLD").split(",")
	prices = fetch_prices(syms)
	assert not prices.empty, "Pas de prix"
	ref = syms[0]
	close = prices[ref].dropna()

	# Calcul des features
	m6  = momentum_6m(close)
	dma = distance_ma200(close)
	v20 = vol20(close)
	z   = zscore(close.pct_change(), 60)
	m50 = ma(close, 50)

	# Vérifs simples
	print("Lignes close:", len(close))
	print("m6 non-nulls:", m6.notna().sum())
	print("dma non-nulls:", dma.notna().sum())
	print("v20 non-nulls:", v20.notna().sum())

	# Assertions minimales
	assert m6.index.equals(close.index), "Index différent (momentum)"
	assert dma.index.equals(close.index), "Index différent (dma200)"
	assert v20.index.equals(close.index), "Index différent (vol20)"

	# Valeurs plausibles (pas de délires)
	assert m6.dropna().between(-1.0, 1.0).mean() > 0.5, "Momentum hors bornes plausibles trop souvent"
	assert (dma.dropna().abs() < 1.0).mean() > 0.8, "Distance MA200 anormale trop souvent"
	assert (v20.dropna() >= 0).all(), "Volatilité négative ??"

	print("✅ FEATURES OK pour", ref)


