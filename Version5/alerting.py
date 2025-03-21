print("Started")
from time import sleep
print(1)
from twilio.twiml.voice_response import  VoiceResponse
print(2)
from twilio.rest import Client
print(3)
from details import sid, num, token
print(4)
print("Library Imported")
# Your Twilio account SID and authentication token
account_sid = sid
auth_token = token

# Your Twilio phone numbers
from_number = num
to_number = ''

def alertFunc(details: list):
    make_phone_call(details[0],details[1])
    pass
    
# Function to create TwiML for the voice call
def create_twiml(weapon,loc):
    twiml = VoiceResponse()
    sleep(1)
    twiml.say(f"A weapon was detected at {loc}. ", voice='alice', language='en-US')
    
    # with twiml.gather(numDigits=1, action='/handle_key', method='POST') as gather:
    #     gather.say("No input received. Goodbye.", voice='alice', language='en-US')
    return str(twiml)

# # Function to handle key presses
# # Function to handle key presses
# def handle_key():
#     twiml = VoiceResponse()
#     twiml.say("You pressed 1. Repeating the phrase.", voice='alice', language='en-US')
#     twiml.redirect('/handle_key', method='POST')  # Corrected line
#     return str(twiml)


# Make a phone call
def make_phone_call(weapon,loc):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        twiml=create_twiml(weapon,loc)
    )
    print(f"Phone call initiated. Call SID: {call.sid}")

if __name__ == "__main__":
    location = "your_location"
    weapon = 'Gun'
    print("About To call")
    sleep(3)
    print("Calling...")
    alertFunc([weapon,location])
