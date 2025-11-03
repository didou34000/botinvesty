from app.sentiment import news_sentiment_score


if __name__ == "__main__":
	positifs = ["Excellent rapport sur les marchés", "Croissance forte et inflation en baisse"]
	negatifs = ["Crise bancaire mondiale", "Inflation en hausse, inquiétudes sur la récession"]
	neutres  = ["Le marché reste stable", "Les investisseurs attendent les décisions"]

	s_pos = news_sentiment_score(positifs)
	s_neg = news_sentiment_score(negatifs)
	s_neu = news_sentiment_score(neutres)

	print("Positif:", s_pos, "| Négatif:", s_neg, "| Neutre:", s_neu)

	# Vérifications de cohérence
	assert 60 <= s_pos <= 100, f"Sentiment positif trop faible: {s_pos}"
	assert 0 <= s_neg <= 60, f"Sentiment négatif trop élevé: {s_neg}"
	assert 30 <= s_neu <= 70, f"Sentiment neutre incohérent: {s_neu}"
	assert s_pos > s_neu > s_neg, "Ordre de cohérence brisé (positif > neutre > négatif)"

	print("SENTIMENT OK - module VADER fonctionne")


