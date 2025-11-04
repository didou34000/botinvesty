import json
import os
import sys
from http.server import BaseHTTPRequestHandler


# Ensure Python can import our market-guard modules
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MG_DIR = os.path.join(ROOT_DIR, "market-guard")
if MG_DIR not in sys.path:
    sys.path.insert(0, MG_DIR)


from app.sources import fetch_prices  # type: ignore
from app.signals import signal_for    # type: ignore


def _analyze_symbol(symbol: str):
    syms = [symbol.upper()]
    prices = fetch_prices(syms, period="1y", interval="1d")
    if prices.empty or symbol.upper() not in prices.columns:
        raise ValueError("no_prices")
    close = prices[symbol.upper()].dropna()
    sig, meta, conf = signal_for(close)
    # Map to verdict and conviction [0,1]
    verdict = "BUY" if sig == "BUY" else ("SELL" if sig == "SELL" else "HOLD")
    conviction = max(0.0, min(1.0, float(conf) / 100.0))
    return {
        "verdict": verdict,
        "conviction": round(conviction, 4),
        "horizon_days": 14,
        "meta": meta,
    }


class handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # noqa: N802
        try:
            # Auth
            api_key_hdr = self.headers.get("x-api-key", "")
            expected = os.getenv("BOT_API_KEY", "")
            if not expected or api_key_hdr != expected:
                self._send(401, {"error": "unauthorized"})
                return

            length = int(self.headers.get("content-length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except Exception:
                self._send(400, {"error": "invalid_json"})
                return

            symbol = str(data.get("symbol", "")).strip().upper()
            if not symbol:
                self._send(400, {"error": "symbol_required"})
                return

            try:
                out = _analyze_symbol(symbol)
            except ValueError as e:
                if str(e) == "no_prices":
                    self._send(404, {"error": "no_prices"})
                else:
                    self._send(500, {"error": "analysis_failed"})
                return

            self._send(200, {
                "verdict": out["verdict"],
                "conviction": out["conviction"],
                "horizon_days": out["horizon_days"],
            })
        except Exception as exc:  # Fallback error
            self._send(500, {"error": "server_error", "detail": str(exc)})


