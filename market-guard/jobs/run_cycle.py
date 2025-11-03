import os, time
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from app.sources import fetch_prices, fetch_macro, fetch_news_texts
from app.features import momentum_6m, distance_ma200, vol20
from app.sentiment import news_sentiment_score
from app.scoring import riskon_score, macrohealth_score, global_score
from app.signals import batch_signals
from app.emailer import send_mail
from app.trigger import maybe_alert_global


def compute_scores_and_signals():
	syms = os.getenv("WATCHLIST","ACWI,QQQ,GLD,BTC-USD").split(",")
	prices = fetch_prices(syms)
	if prices.empty:
		raise RuntimeError("Pas de prix récupérés. Vérifie WATCHLIST et Internet.")
	# --- RiskOn (sur ACWI si dispo, sinon 1er)
	ref = "ACWI" if "ACWI" in prices.columns else prices.columns[0]
	close = prices[ref].dropna()
	mom12 = momentum_6m(close)
	dist200 = distance_ma200(close)
	v20s = vol20(close)
	risk_s = riskon_score(mom12, dist200, v20s)

	# --- Macro
	macro = fetch_macro()
	cpi_trend = macro["CPI"].pct_change(12).iloc[-1] if "CPI" in macro else 0.0
	pmi = 50.0  # placeholder (à raffiner plus tard)
	curve = (macro["DGS10"].iloc[-1]-macro["DGS2"].iloc[-1]) if {"DGS10","DGS2"}.issubset(macro.columns) else 0.0
	un_trend = macro["UNEMP"].pct_change(12).iloc[-1] if "UNEMP" in macro else 0.0
	macro_s = macrohealth_score(cpi_trend, pmi, curve, un_trend)

	# --- News
	texts = fetch_news_texts()
	news_s = news_sentiment_score(texts)

	# --- Global
	g = global_score(macro_s, risk_s, news_s, weights=(0.4,0.4,0.2))

	# --- Signaux par actif
	signals_df = batch_signals(prices)

	return {
		"scores": {"risk":risk_s, "macro":macro_s, "news":news_s, "global":g},
		"signals_df": signals_df
	}


def format_email(state_word, pack):
	s = pack["scores"]
	df = pack["signals_df"].copy()
	# garde 10 lignes max
	df = df.head(10)
	table_html = df.to_html(index=False, float_format=lambda x: f"{x:.4f}" if isinstance(x,float) else x)

	title = f"[MarketGuard] Fenêtre {'d’achat' if state_word=='RENFORCER' else 'd’allègement'} — Global {s['global']:.1f}/100 (confirmé)"
	body = f"""
	<h2>🧭 Climat : {s['global']:.1f}/100 — <b>{state_word}</b></h2>
	<ul>
	  <li>RiskOn: {s['risk']:.1f}</li>
	  <li>MacroHealth: {s['macro']:.1f}</li>
	  <li>NewsSentiment: {s['news']:.1f}</li>
	</ul>
	<p>Action: {'Renforcer progressivement (2–4 semaines) sur actions/ETF cœur' if state_word=='RENFORCER' else 'Alléger / augmenter la part de cash' }.</p>
	<h3>Signaux watchlist</h3>
	{table_html}
	<hr/>
	<small>Règles: hystérésis, debounce {os.getenv('DEBOUNCE_RUNS','2')} runs, cooldown global {os.getenv('COOLDOWN_GLOBAL_DAYS','3')} j.</small>
	"""
	return title, body


def one_pass():
	pack = compute_scores_and_signals()
	g = pack["scores"]["global"]
	subs = {"risk":pack["scores"]["risk"], "macro":pack["scores"]["macro"], "news":pack["scores"]["news"]}

	def sender(state_word, gscore, subscores):
		title, body = format_email(state_word, pack)
		send_mail(title, body)

	maybe_alert_global(g, subs, sender)
	# Logging console
	print(f"RiskOn: {subs['risk']:.1f} | Macro: {subs['macro']:.1f} | News: {subs['news']:.1f} | Global: {g:.1f}")


if __name__ == "__main__":
	# Mode par défaut: 1 passe. Pour boucler, param LOOP_MINUTES ou argument --loop N
	import argparse
	p = argparse.ArgumentParser()
	p.add_argument("--loop", type=int, default=int(os.getenv("LOOP_MINUTES","0")), help="Minutes entre deux passes (0 = une seule passe)")
	args = p.parse_args()

	if args.loop and args.loop > 0:
		print(f"⏳ Mode boucle: une passe toutes {args.loop} minutes. Ctrl+C pour arrêter.")
		while True:
			try:
				one_pass()
			except Exception as e:
				print("Erreur lors d'une passe:", e)
			time.sleep(args.loop * 60)
	else:
		one_pass()

