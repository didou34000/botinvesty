import os, json
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

try:
	from openai import OpenAI
	_HAS_OPENAI = True
except Exception:
	_HAS_OPENAI = False


SYSTEM_PROMPT = (
	"Tu es un analyste macro-financier professionnel.\n"
	"- Entrées: sous-scores (RiskOn/Macro/News), GlobalScore, 10-25 titres d'actualités récents, tableau des signaux (BUY/SELL/HOLD).\n"
	"- Règles: prudence, pas d'invention de chiffres, pas d'affirmations gratuites.\n"
	"- Réponds en JSON STRICT: {\\\"verdict\\\":\\\"CONFIRMER|NUANCER|INFIRMER\\\",\\\"rationale\\\":\\\"...\\\",\\\"key_points\\\":[\\\"...\\\"],\\\"risk_watchlist\\\":[\\\"...\\\"]}.\n"
	"- 'verdict' = CONFIRMER si le contexte justifie le signal, NUANCER si mitigé, INFIRMER si contradictoire.\n"
	"- Style: concis (3-5 phrases max)."
)


def _payload(scores: Dict[str,float], news_titles: List[str], signals_records: List[Dict[str,Any]]) -> str:
	return json.dumps({
		"scores": scores,
		"news_titles": news_titles[:25],
		"signals": signals_records[:8]
	}, ensure_ascii=False)


def _call_openai(system_prompt: str, user_payload: str, model: str, max_tokens: int) -> str:
	proj = os.getenv("OPENAI_PROJECT")
	client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=proj) if proj else OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
	r = client.chat.completions.create(
		model=model,
		messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_payload}],
		temperature=0.2,
		max_tokens=max_tokens
	)
	return r.choices[0].message.content


def generate_market_commentary(scores: Dict[str,float], news_titles: List[str], signals_records: List[Dict[str,Any]]) -> Dict[str, Any]:
	if os.getenv("ENABLE_AI_ANALYST","false").lower() != "true" or (not _HAS_OPENAI) or (not os.getenv("OPENAI_API_KEY")):
		return {"verdict":"NUANCER","rationale":"IA désactivée ou non configurée.","key_points":[],"risk_watchlist":[]}
	try:
		raw = _call_openai(
			system_prompt=SYSTEM_PROMPT,
			user_payload=_payload(scores, news_titles, signals_records),
			model=os.getenv("AI_MODEL","gpt-5"),
			max_tokens=int(os.getenv("AI_MAX_TOKENS","600"))
		)
		s, e = raw.find("{"), raw.rfind("}")
		if s >= 0 and e > s: raw = raw[s:e+1]
		data = json.loads(raw)
		verdict = str(data.get("verdict","NUANCER")).upper()
		if verdict not in ("CONFIRMER","NUANCER","INFIRMER"): verdict = "NUANCER"
		return {
			"verdict": verdict,
			"rationale": str(data.get("rationale","")).strip(),
			"key_points": list(data.get("key_points",[]))[:5],
			"risk_watchlist": list(data.get("risk_watchlist",[]))[:5]
		}
	except Exception as e:
		return {"verdict":"NUANCER","rationale":f"Echec IA: {e}. Utiliser les scores.","key_points":[],"risk_watchlist":[]}


