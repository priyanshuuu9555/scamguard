import json
import re
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

API_KEY = "my-honeypot-key"

# ---------------- SCAM KNOWLEDGE ----------------

SCAM_TYPES = {
    "bank_kyc": [
        "kyc", "account blocked", "verify account",
        "update details", "bank alert"
    ],
    "otp": [
        "otp", "one time password", "verification code"
    ],
    "prize": [
        "prize", "lottery", "won", "reward", "congratulations"
    ],
    "upi_refund": [
        "upi", "refund", "payment failed", "reverse transaction"
    ],
    "job": [
        "job offer", "work from home", "earn money",
        "registration fee"
    ]
}

def detect_scam_type(message):
    for scam_type, keywords in SCAM_TYPES.items():
        for word in keywords:
            if word in message:
                return scam_type
    return "unknown"

# ---------------- AGENTIC REPLIES ----------------

HUMAN_REPLIES = {
    1: [
        "I didn’t understand this properly, can you explain again?",
        "Sorry, I am a bit confused. What should I do?"
    ],
    2: [
        "I tried what you said but it is showing some error.",
        "It’s not working on my phone, can you guide me?"
    ],
    3: [
        "Where exactly should I send the payment?",
        "Can you share the account or UPI details again?"
    ],
    4: [
        "I am trying again, please wait.",
        "It’s taking time, my network is slow."
    ]
}

# ---------------- INTELLIGENCE EXTRACTION ----------------

def extract_intelligence(message):
    return {
        "upi_ids": re.findall(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]+", message),
        "bank_accounts": re.findall(r"\b\d{9,18}\b", message),
        "phishing_links": re.findall(r"https?://\S+", message)
    }

# ---------------- BASIC HOME ----------------

def home(request):
    return HttpResponse("ScamGuard API is running")

# ---------------- MAIN API ----------------

@csrf_exempt
def detect_scam(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    api_key = request.headers.get("X-API-KEY") or request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}

    message = data.get("message", "").lower()

    # ✅ REQUIRED FOR HACKATHON TESTER
    if not message:
        return JsonResponse({
            "status": "ok",
            "message": "Honeypot endpoint reachable",
            "agent_active": False
        })

    try:
        turn = int(data.get("turn", 1))
    except (ValueError, TypeError):
        turn = 1

    scam_type = detect_scam_type(message)
    scam_detected = scam_type != "unknown"

    if scam_detected:
        replies = HUMAN_REPLIES.get(turn, HUMAN_REPLIES[4])
        reply = replies[0]
        stage = turn
    else:
        reply = "Okay, thanks for the information."
        stage = 0

    extracted = extract_intelligence(message)

    return JsonResponse({
        "scam_detected": scam_detected,
        "scam_type": scam_type,
        "agent_active": scam_detected,
        "conversation_stage": stage,
        "reply": reply,
        "extracted_intelligence": extracted
    })
