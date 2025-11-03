from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


analyzer = SentimentIntensityAnalyzer()


def news_sentiment_score(texts):
	"""
	Calcule un score de sentiment global (0-100) à partir d'une liste de textes.
	Utilise le 'compound score' de VADER, borné à [-0.6, +0.6].
	Retourne 50 si aucun texte valide.
	"""
	if not texts:
		return 50.0
	scores = [analyzer.polarity_scores(t)["compound"] for t in texts if t.strip()]
	if not scores:
		return 50.0
	m = float(np.mean(scores))  # moyenne des composés (-1..+1)
	lo, hi = -0.6, 0.6
	m = max(lo, min(hi, m))
	return 100.0 * (m - lo) / (hi - lo)


