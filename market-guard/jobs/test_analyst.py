from app.analyst import generate_market_commentary


if __name__ == "__main__":
	scores = {"risk":62.1,"macro":57.4,"news":55.2,"global":59.5}
	news = ["La Fed laisse les taux inchangés","ISM proche de 50","Résultats solides dans la tech"]
	signals = [{"Ticker":"ACWI","Signal":"BUY","Confidence":78.5},{"Ticker":"QQQ","Signal":"BUY","Confidence":80.2}]
	out = generate_market_commentary(scores, news, signals)
	print(out)


