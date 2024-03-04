from flask.app import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse, Say, Gather
import os

sales_number = os.getenv("SALES_NUMBER")
support_number = os.getenv("SUPPORT_NUMBER")
from_number = os.getenv("FROM_NUMBER")

print(f"Sales number: {sales_number}")
print(f"Support number: {support_number}")
print(f"From number: {from_number}")

app = Flask(__name__)

VOICE = "Google.en-US-Neural2-A"
LANGUAGE = "en-US"

@app.route("/twiml", methods=["POST"])
def twiml_route():
    twiml = VoiceResponse()
    twiml.say("Thank you for calling Owl Labs!", voice=VOICE, language=LANGUAGE)
    gather = Gather(action="/gather", method="POST", num_digits="1")
    gather.say(
        "Press 1 to speak to sales or press 2 to speak with support",
        voice=VOICE,
        language=LANGUAGE,
    )
    twiml.append(gather)
    return Response(str(twiml), mimetype="application/xml")

@app.route("/gather", methods=["POST"])
def gather_route():
    digits = request.form.get("Digits")
    twiml = VoiceResponse()
    
    match digits:
        case "1":
            twiml.say("OK, connecting you to sales.", voice=VOICE, language=LANGUAGE)
            twiml.dial(sales_number, caller_id=from_number)
            return Response(str(twiml), mimetype="application/xml")

        case "2":
            twiml.say("OK, connecting you to support.", voice=VOICE, language=LANGUAGE)
            twiml.dial(support_number, caller_id=from_number)
            return Response(str(twiml), mimetype="application/xml")