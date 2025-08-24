import os
import time
import logging
from twilio.rest import Client
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Twilio account details from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'ACd6da0c2c447f7dbf8b36380a527cbfd5')
auth_token = os.getenv('TWILIO_AUTH_TOKEN', '5fc9600cf81ed30797d209babe1407cd')
client = Client(account_sid, auth_token)

# Firebase credentials from environment variables
firebase_cred_path = os.getenv('FIREBASE_CRED_PATH', 'twilio-twilio-python-0f81bbb/firebasekey.json')

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    initialize_firebase()
    return firestore.client()

def store_coordinates(latitude, longitude):
    try:
        db = get_firestore_client()
        doc_ref = db.collection('coordinates').document()
        doc_ref.set({
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        logging.info(f"Coordinates stored with ID: {doc_ref.id}")
    except Exception as e:
        logging.error(f"Error storing coordinates: {e}")

def send_emergency_sms_with_location(latitude, longitude, recipient_number):
    try:
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        message_body = f"Emergency! Help is needed at the following location: {maps_link}"
        message = client.messages.create(
            body=message_body,
            from_='+12085162644',
            to=recipient_number
        )
        store_coordinates(latitude, longitude)
        logging.info(f"SMS sent! SID: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending SMS: {e}")

def send_periodic_location_updates(latitude, longitude, recipient_number, interval_minutes):
    for _ in range(10):
        send_emergency_sms_with_location(latitude, longitude, recipient_number)
        time.sleep(interval_minutes * 60)

@app.route('/send-location', methods=['POST'])
def send_location_and_call():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        recipient_number = data.get('recipient_number', '+91 9766966511')

        if not latitude or not longitude:
            return jsonify({"status": "error", "message": "Latitude and longitude are required"}), 400

        call = client.calls.create(
            to=recipient_number,
            from_='+15673613362',
            twiml='<Response><Say>Help, this is an emergency. Please assist immediately. Help, this is an emergency. Please assist immediately. Help, this is an emergency. Please assist immediately.</Say></Response>'
        )
        logging.info(f"Call initiated with SID: {call.sid}")

        send_emergency_sms_with_location(latitude, longitude, recipient_number)

        threading.Thread(target=send_periodic_location_updates, args=(latitude, longitude, recipient_number, 1), daemon=True).start()

        return jsonify({"status": "success", "message": "Emergency call made and location sent"}), 200
    except Exception as e:
        logging.error(f"Error in /send-location: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/send-emergency-call', methods=['POST'])
def send_emergency_call():
    try:
        data = request.json
        recipient_number = data.get('recipient_number', '+91 9766966511')

        call = client.calls.create(
            to=recipient_number,
            from_='+15673613362',
            twiml='''
            <Response>
                <Say>Help, this is an emergency. Please assist immediately.</Say>
                <Record maxLength="30" playBeep="true" />
                <Say>Thank you for recording. Goodbye.</Say>
            </Response>
            ''',
            record=True
        )

        logging.info(f"Call initiated with SID: {call.sid}")

        return jsonify({
            "status": "success", 
            "message": "Emergency call made with recording",
            "call_sid": call.sid
        }), 200
    except Exception as e:
        logging.error(f"Error in /send-emergency-call: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5002)