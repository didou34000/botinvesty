import numpy as np
import pandas as pd
from app.features import momentum_6m, vol20


def adaptive_ma_window(close: pd.Series) -> int:
	""" Calcule une fenêtre de MA adaptative basée sur la volatilité 60j.
		Plus la vol est élevée, plus on lisse (fenêtre longue).
		Fenêtre bornée entre 60 et 250. """
	vol_60 = close.pct_change().rolling(60).std().iloc[-1]
	base = 100.0
	w = int(np.clip(base * (0.01 / max(1e-6, vol_60)), 60, 250))
	return w


def signal_for(close: pd.Series):
	""" Renvoie (signal, meta, confidence)
		signal ∈ {BUY, HOLD, SELL}
		meta: dict {ma_w, dist, mom6m, vol20, ma, price}
		confidence: 0–100 selon la force du momentum et l'écart à la MA. """
	if close is None or close.dropna().empty:
		return "HOLD", {"reason": "no_data"}, 0.0

	close = close.dropna()
	w = adaptive_ma_window(close)
	ma = close.rolling(w).mean()
	price = close.iloc[-1]
	ma_last = ma.iloc[-1]

	if np.isnan(ma_last):
		return "HOLD", {"reason": "ma_nan"}, 0.0

	dist = price / ma_last - 1.0
	mom6 = momentum_6m(close).iloc[-1]
	v20s = vol20(close)
	v20_last = v20s.iloc[-1]
	v20_med  = v20s.rolling(252).median().iloc[-1] if len(v20s.dropna())>252 else v20s.median()

	# Règles
	buy  = (dist > 0) and (mom6 > 0)
	sell = (dist < 0) and (v20_last > 1.2 * v20_med)

	sig = "BUY" if buy else ("SELL" if sell else "HOLD")

	# Confiance (0–100)
	# - plus |dist| est grand et plus mom6 est positif/négatif, plus la confiance est forte
	conf_dist = float(np.interp(abs(dist), [0.0, 0.10], [20, 80]))     # 0..10% au-dessus/-dessous MA
	conf_mom  = float(np.interp(abs(mom6), [0.0, 0.20], [10, 80]))     # 0..20% 6m change
	conf_vol  = float(np.interp(v20_last / max(1e-6, v20_med), [0.8, 1.2, 2.0], [70, 50, 20])) if sig=="SELL" else 50
	confidence = np.clip((conf_dist + conf_mom + conf_vol) / 2.0, 0, 100) if sig!="HOLD" else float(np.clip(50 - 100*abs(dist), 5, 60))

	meta = {
		"ma_w": int(w),
		"price": float(price),
		"ma": float(ma_last),
		"dist": float(dist),
		"mom6m": float(mom6),
		"vol20": float(v20_last),
		"vol20_med": float(v20_med)
	}
	return sig, meta, float(confidence)


def batch_signals(prices: pd.DataFrame) -> pd.DataFrame:
	""" Applique signal_for à toutes les colonnes d'un DataFrame de prix. """
	rows = []
	if prices is None or prices.empty:
		return pd.DataFrame(columns=["Ticker","Signal","Confidence","ma_w","price","ma","dist","mom6m","vol20","vol20_med"])
	for col in prices.columns:
		sig, meta, conf = signal_for(prices[col])
		rows.append({
			"Ticker": col,
			"Signal": sig,
			"Confidence": conf,
			**meta
		})
	df = pd.DataFrame(rows)
	return df.sort_values(["Signal","Confidence"], ascending=[True, False]).reset_index(drop=True)

