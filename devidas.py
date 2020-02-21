# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, request
import requests

# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 

PAGE_ACCESS_TOKEN = "EAATY6rePVFgBAPnDparTaK4sZCPP5zE2JZCGiU9oHYkapJZCStyzd4sn9CoMZB0pGMu8ZAffB9NZASVTCyi9cpM8S379wErZBg3tkyMoHOIZAa9RPxrZCp6IcR1zTjZBHn8yL9Ev3eqkxWbB9ezyUbgiJFqt8fwS2qujNSZCPvLSLO7gzVaNJzDJDFq"

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)

def verify_webhook(req):
    if req.args.get("hub.verify_token") == "password":
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)
    
def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook")
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
   # port = int(os.environ.get("PORT", 5000))
    app.run() 