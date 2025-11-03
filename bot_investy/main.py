from __future__ import annotations

import argparse
import logging

from .config import AppConfig


def configure_logging(level: str) -> None:
	numeric_level = getattr(logging, level.upper(), logging.INFO)
	logging.basicConfig(
		level=numeric_level,
		format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
	)


def run(strategy: str, symbol: str) -> int:
	config = AppConfig.load()
	configure_logging(config.log_level)
	logger = logging.getLogger("bot_investy")

	logger.info("Starting bot", extra={})
	logger.info("Config loaded: data_source=%s base_currency=%s", config.data_source, config.base_currency)
	logger.info("Selected strategy=%s symbol=%s", strategy, symbol)

	# Placeholder: implement data fetching and strategy execution
	logger.info("(placeholder) Fetching data for %s from %s", symbol, config.data_source)
	logger.info("(placeholder) Running strategy %s", strategy)

	logger.info("Done")
	return 0


def main() -> int:
	parser = argparse.ArgumentParser(description="botinvesty - Simple investment bot skeleton")
	parser.add_argument("symbol", help="Ticker symbol, e.g., AAPL")
	parser.add_argument("--strategy", default="sample", help="Strategy name to run")
	args = parser.parse_args()
	return run(strategy=args.strategy, symbol=args.symbol)


if __name__ == "__main__":
	raise SystemExit(main())


