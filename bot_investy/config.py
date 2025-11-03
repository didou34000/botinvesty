from __future__ import annotations

from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os


class AppConfig(BaseModel):
	# Example config fields; extend as needed
	data_source: str = Field(default="mock", description="Data provider identifier")
	base_currency: str = Field(default="USD")
	log_level: str = Field(default="INFO")

	api_key: str | None = Field(default=None, description="Optional API key for data providers")

	@staticmethod
	def load() -> "AppConfig":
		load_dotenv()
		return AppConfig(
			data_source=os.getenv("DATA_SOURCE", "mock"),
			base_currency=os.getenv("BASE_CURRENCY", "USD"),
			log_level=os.getenv("LOG_LEVEL", "INFO"),
			api_key=os.getenv("API_KEY"),
		)


