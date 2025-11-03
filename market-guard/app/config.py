from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
	RESEND_API_KEY: str
	MAIL_TO: str

	FRED_API_KEY: Optional[str]
	WATCHLIST: List[str]

	GLOBAL_HI: int
	GLOBAL_LO: int
	DEBOUNCE_RUNS: int
	COOLDOWN_GLOBAL_DAYS: int
	COOLDOWN_ASSET_DAYS: int
	NEWS_MIN_FOR_BUY: int


_settings_singleton: Settings | None = None


def _parse_watchlist(raw: str | None) -> List[str]:
	if not raw:
		return ["ACWI", "QQQ", "GLD", "BTC-USD"]
	items = [s.strip() for s in raw.split(",")]
	return [s for s in items if s]


def get_settings() -> Settings:
	global _settings_singleton
	if _settings_singleton is not None:
		return _settings_singleton

	# Load environment variables from .env if present
	load_dotenv()

	settings = Settings(
		RESEND_API_KEY=os.getenv("RESEND_API_KEY", ""),
		MAIL_TO=os.getenv("MAIL_TO", ""),
		FRED_API_KEY=os.getenv("FRED_API_KEY"),
		WATCHLIST=_parse_watchlist(os.getenv("WATCHLIST")),
		GLOBAL_HI=int(os.getenv("GLOBAL_HI", "72")),
		GLOBAL_LO=int(os.getenv("GLOBAL_LO", "28")),
		DEBOUNCE_RUNS=int(os.getenv("DEBOUNCE_RUNS", "2")),
		COOLDOWN_GLOBAL_DAYS=int(os.getenv("COOLDOWN_GLOBAL_DAYS", "3")),
		COOLDOWN_ASSET_DAYS=int(os.getenv("COOLDOWN_ASSET_DAYS", "7")),
		NEWS_MIN_FOR_BUY=int(os.getenv("NEWS_MIN_FOR_BUY", "55")),
	)

	_settings_singleton = settings
	return settings


def validate_required(settings: Settings | None = None) -> None:
	cfg = settings or get_settings()
	missing = []
	if not cfg.RESEND_API_KEY:
		missing.append("RESEND_API_KEY")
	if not cfg.MAIL_TO:
		missing.append("MAIL_TO")
	if missing:
		raise ValueError(f"Missing required settings: {', '.join(missing)}")


