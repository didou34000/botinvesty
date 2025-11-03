import numpy as np


def _clip01(x): 
	return float(np.clip(x, 0.0, 100.0))


def riskon_score(momentum12m, dist_ma200, vol20):
	""" Agrège 3 séries (m, d, v) en score 0–100.
		- momentum12m ~ variation 12m (en décimal)
		- dist_ma200 ~ close/MA200 - 1
		- vol20 ~ écart-type 20j des retours (décimal)
	"""
	m = float(np.nanmedian(momentum12m) * 100.0)  # % approx
	d = float(np.nanmedian(dist_ma200) * 100.0)   # %
	v = float(np.nanmedian(vol20) * 100.0)        # %

	s_m = np.interp(m, [-40, 40], [0, 100])   # [-40% ; +40%] -> [0;100]
	s_d = np.interp(d, [-20, 20], [0, 100])   # [-20% ; +20%] -> [0;100]
	s_v = np.interp(v, [40, 0],  [0, 100])    # 40% -> 0 ; 0% -> 100 (moins de vol = mieux)

	return _clip01(0.5*s_m + 0.3*s_d + 0.2*s_v)


def macrohealth_score(cpi_trend, pmi, curve_2y10y, unemp_trend):
	""" Entrées: variations annuelles (CPI, chômage), PMI (≈40–60), pente courbe (≈-2% à +2%).
	 Renvoie 0–100. """
	s_cpi = np.interp(-100*cpi_trend, [0, 2], [0, 100])   # -2 pp d'inflation -> bon (map 0..2)
	s_pmi = np.interp(pmi, [40, 60], [0, 100])
	s_cv  = np.interp(100*curve_2y10y, [-2, 2], [0, 100]) # -2%..+2%
	s_ue  = np.interp(-100*unemp_trend, [0, 1], [0, 100]) # -1 pp de chômage -> bon
	vals = [s_cpi, s_pmi, s_cv, s_ue]
	return _clip01(float(np.nanmean(vals)))


def global_score(macro, riskon, news, weights=(0.4, 0.4, 0.2)):
	m, r, n = macro, riskon, news
	w0, w1, w2 = weights
	return _clip01(w0*m + w1*r + w2*n)


