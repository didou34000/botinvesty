from __future__ import annotations

import sys

from app.config import get_settings, validate_required


def _mask_resend(api_key: str) -> str:
	if not api_key:
		return "(empty)"
	if not api_key.startswith("re_"):
		# generic mask
		return (api_key[:2] + "****" + api_key[-4:]) if len(api_key) > 6 else "****"
	return "re_****" + api_key[-4:]


def main() -> int:
	try:
		cfg = get_settings()
		print("Settings loaded:")
		print("  RESEND_API_KEY:", _mask_resend(cfg.RESEND_API_KEY))
		print("  MAIL_TO:", cfg.MAIL_TO or "(empty)")
		print("  FRED_API_KEY:", "(set)" if cfg.FRED_API_KEY else "(empty)")
		print("  WATCHLIST:", ",".join(cfg.WATCHLIST))
		print("  GLOBAL_HI:", cfg.GLOBAL_HI)
		print("  GLOBAL_LO:", cfg.GLOBAL_LO)
		print("  DEBOUNCE_RUNS:", cfg.DEBOUNCE_RUNS)
		print("  COOLDOWN_GLOBAL_DAYS:", cfg.COOLDOWN_GLOBAL_DAYS)
		print("  COOLDOWN_ASSET_DAYS:", cfg.COOLDOWN_ASSET_DAYS)
		print("  NEWS_MIN_FOR_BUY:", cfg.NEWS_MIN_FOR_BUY)

		# validation
		validate_required(cfg)
		print("DOTENV OK")
		return 0
	except Exception as exc:
		print("Config error:", str(exc))
		return 1


if __name__ == "__main__":
	raise SystemExit(main())


