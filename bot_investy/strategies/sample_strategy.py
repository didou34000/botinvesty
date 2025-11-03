from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SampleStrategy:
	name: str = "sample"

	def generate_signal(self, prices: list[float]) -> str:
		if not prices:
			return "HOLD"
		# Naive placeholder rule: if last price is above the average -> BUY else SELL
		avg = sum(prices) / len(prices)
		return "BUY" if prices[-1] > avg else "SELL"


