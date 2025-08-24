from twilio.rest import Client

# Twilio account details
ACCOUNT_SID = 'ACd6da0c2c447f7dbf8b36380a527cbfd5'
AUTH_TOKEN = '5fc9600cf81ed30797d209babe1407cd'
TWILIO_PHONE_NUMBER = '+15673613362'  # Replace with your Twilio phone number

# Initialize Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(recipient_number, message_body):
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        print(f"SMS sent! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def make_call(recipient_number):
    try:
        call = client.calls.create(
            to=recipient_number,
            from_=TWILIO_PHONE_NUMBER,
            twiml='<Response><Say>This is an emergency call. Please respond immediately. This is an emergency call. Please respond immediately. This is an emergency call. Please respond immediately.</Say></Response>'
        )
        print(f"Call initiated! SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make call: {e}")

if __name__ == "__main__":
    # Hardcoded recipient number
    recipient_number = "+91 9766966511"
    
    # Send SMS
    message_body = "Emergency alert! Please respond immediately."
    send_sms(recipient_number, message_body)
    
    # Make Call
    make_call(recipient_number)
