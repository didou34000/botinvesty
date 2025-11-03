import sys

mods = [
	"pandas",
	"numpy",
	"yfinance",
	"fredapi",
	"feedparser",
	"vaderSentiment",
	"dotenv",
	"requests",
	"resend",
]

missing = []
for m in mods:
	try:
		__import__(m)
	except Exception as e:
		missing.append((m, str(e)))

print("Python:", sys.version)
if missing:
	print("Missing/Errors:", missing)
	raise SystemExit(1)
else:
	print("ENV OK")


