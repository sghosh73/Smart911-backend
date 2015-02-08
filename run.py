from flask import Flask, request, redirect
from firebase import firebase
import twilio.twiml
import json
 
app = Flask(__name__)
 
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    from_number = request.values.get('From', None)
    caller = "Monkey"
 
    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hello ")
    # Play an mp3
    resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")
 
    # Say a command, and listen for the caller to press a key. When they press
    # a key, redirect them to /handle-key.
    with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
        g.say("To speak to a real person, press 1.")
 
    return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = twilio.twiml.Response()


        firebase = firebase.FirebaseApplication('https://smart911.firebaseio.com', None)
        result = firebase.get('/operators', None)

        for operator in result:
        	if result[operator.encode('ascii')][online] == True:
        		resp.dial("+" + str(result[operator.encode('ascii')][number]))
        		return str(resp)



        # resp.dial("+14086411239")
        # If the dial fails:
        resp.say("Sorry, no operator is available")
 
        return redirect("/")
 
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")
 
if __name__ == "__main__":
    app.run(debug=True)