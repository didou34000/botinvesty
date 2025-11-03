import os
import pandas as pd
import yfinance as yf
import feedparser
from datetime import datetime
from fredapi import Fred
from dotenv import load_dotenv


load_dotenv()


def fetch_prices(symbols, period="5y", interval="1d") -> pd.DataFrame:
	data: dict[str, pd.Series] = {}
	for s in symbols:
		# Force auto_adjust=False pour stabilité et éviter le FutureWarning
		df = yf.download(s, period=period, interval=interval, progress=False, auto_adjust=False)
		if df is None:
			continue
		# Cas DataFrame standard avec colonne Close
		if isinstance(df, pd.DataFrame) and "Close" in df.columns and not df["Close"].empty:
			ser = df["Close"].astype(float).squeeze()
			ser.name = s
			data[s] = ser
		# Cas rarissime: yfinance peut retourner une Series
		elif isinstance(df, pd.Series) and not df.empty:
			ser = pd.Series(df.astype(float))
			ser.name = s
			data[s] = ser

	if not data:
		return pd.DataFrame()

	out = pd.DataFrame(data).dropna(how="all")
	if not out.empty:
		out.index = pd.to_datetime(out.index)
	return out


def fetch_macro() -> pd.DataFrame:
    api_key = os.getenv("FRED_API_KEY")
    # Fallback si clé absente/incorrecte: renvoyer DF vide
    if not api_key or not (len(api_key) == 32 and api_key.isalnum() and api_key == api_key.lower()):
        return pd.DataFrame()
    try:
        fred = Fred(api_key=api_key)
        d10 = fred.get_series("DGS10")   # taux US 10 ans
        d2  = fred.get_series("DGS2")    # taux US 2 ans
        un  = fred.get_series("UNRATE")  # chômage
        cpi = fred.get_series("CPIAUCSL")  # inflation
        df = pd.concat([
            pd.Series(d10, name="DGS10"),
            pd.Series(d2, name="DGS2"),
            pd.Series(un, name="UNEMP"),
            pd.Series(cpi, name="CPI")
        ], axis=1)
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    except Exception:
        # En cas d'erreur réseau/clé invalide, fallback silencieux
        return pd.DataFrame()


def fetch_news_texts(rss_urls=None, max_items=100):
	if rss_urls is None:
		rss_urls = [
			"https://www.lesechos.fr/rss/rss_finance-marches.xml",
			"https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
			"https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
		]
	texts = []
	for url in rss_urls:
		d = feedparser.parse(url)
		for e in d.entries[:max_items]:
			title = getattr(e, "title", "") or ""
			summary = getattr(e, "summary", "") or ""
			texts.append(f"{title}. {summary}")
	return texts[:max_items]

