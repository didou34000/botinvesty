import pandas as pd
import numpy as np


# --- Utils ---
def clamp(v: float, lo: float, hi: float) -> float:
	return float(max(lo, min(hi, v)))


def zscore(series: pd.Series, window: int = 60) -> pd.Series:
	mu = series.rolling(window).mean()
	sd = series.rolling(window).std()
	return (series - mu) / sd


# --- Features principales ---
def momentum_6m(close: pd.Series) -> pd.Series:
	# ~ 6 mois de bourse ~ 126 séances
	return close.pct_change(126)


def distance_ma200(close: pd.Series) -> pd.Series:
	ma = close.rolling(200).mean()
	return (close / ma) - 1.0


def vol20(close: pd.Series) -> pd.Series:
	return close.pct_change().rolling(20).std()


# --- Sanity helpers ---
def pct_change_n(close: pd.Series, n: int) -> pd.Series:
	return close.pct_change(n)


def ma(close: pd.Series, window: int) -> pd.Series:
	return close.rolling(window).mean()

