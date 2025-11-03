import os, json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def load_state(path="state/global.json"):
	try:
		with open(path,"r") as f:
			return json.load(f)
	except:
		return {"global_state":"NEUTRE","last_global_mail":None,"pending_hi":0,"pending_lo":0}


def save_state(st, path="state/global.json"):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path,"w") as f:
		json.dump(st,f)


def days_since(iso):
	if not iso:
		return 9999
	try:
		return (datetime.utcnow() - datetime.fromisoformat(iso)).days
	except:
		return 9999


def maybe_alert_global(global_score, subscores, send_fn):
	"""Décide s'il faut envoyer une alerte en fonction du global_score.
	   send_fn(state_word, global_score, subscores) sera appelée si besoin."""
	HI = int(os.getenv("GLOBAL_HI","72"))
	LO = int(os.getenv("GLOBAL_LO","28"))
	DEB = int(os.getenv("DEBOUNCE_RUNS","2"))
	CD  = int(os.getenv("COOLDOWN_GLOBAL_DAYS","3"))

	st = load_state()

	# Zone haute = renforcer
	if global_score >= HI:
		st["pending_hi"] += 1
		st["pending_lo"] = 0
		if st["global_state"] in ("NEUTRE","ALLEGER") and st["pending_hi"] >= DEB and days_since(st["last_global_mail"]) >= CD:
			send_fn("RENFORCER", global_score, subscores)
			st["global_state"] = "RENFORCER"
			st["last_global_mail"] = datetime.utcnow().isoformat()

	# Zone basse = alléger
	elif global_score <= LO:
		st["pending_lo"] += 1
		st["pending_hi"] = 0
		if st["global_state"] in ("NEUTRE","RENFORCER") and st["pending_lo"] >= DEB and days_since(st["last_global_mail"]) >= CD:
			send_fn("ALLEGER", global_score, subscores)
			st["global_state"] = "ALLEGER"
			st["last_global_mail"] = datetime.utcnow().isoformat()

	# Zone neutre
	else:
		st["pending_hi"] = 0
		st["pending_lo"] = 0
		st["global_state"] = "NEUTRE"

	save_state(st)


