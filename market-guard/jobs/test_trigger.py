import os, json, time
from app.trigger import maybe_alert_global, load_state


if __name__ == "__main__":
	def fake_send(state, g, subs):
		print(f"🚀 FAKE ALERT: {state} — score={g:.1f}")

	subs = {"risk":60,"macro":50,"news":55}

	print("Premier passage -> rien")
	maybe_alert_global(80, subs, fake_send)

	print("Deuxième passage -> alerte probable")
	maybe_alert_global(80, subs, fake_send)

	print("État global après test:")
	print(json.dumps(load_state(), indent=2))


