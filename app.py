import os, httplib, urllib, urllib2
import twilio.twiml
from oauth import oauth
from flask import Flask, request, redirect
from datetime import date

from credentials import CONSUMER_KEY, CONSUMER_SECRET
import config

SERVER = 'api.fitbit.com'
ACCESS_TOKEN_STRING_FNAME = 'access_token.string'

DEBUG = True

app = Flask(__name__)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_kg(entered_weight):
    # Fitbit interprets numbers submitted as kg. Convert lb -> kg if needed
    if config.usePounds == True:
        kg = float(entered_weight) * 0.453592
        return kg
    else: return entered_weight

def create_sms(message):
    resp = twilio.twiml.Response()
    resp.sms(message)
    if DEBUG: print resp
    return str(resp)
 
@app.route('/sms', methods=['POST'])
def main():

    connection = httplib.HTTPSConnection(SERVER)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)

    ''' Fitbit API doesn't accept hmac-sha1; use plain text '''
    #signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()

    if DEBUG: print '* Reading file', ACCESS_TOKEN_STRING_FNAME
    fobj = open(ACCESS_TOKEN_STRING_FNAME)
    access_token_string = fobj.read()
    fobj.close()
    access_token = oauth.OAuthToken.from_string(access_token_string)
    
    # Grab incoming info from text messages
    from_number = request.form['From']
    todays_weight = request.form['Body']
    mydate = date.today().isoformat()

    if from_number in config.callers and is_number(todays_weight) == True:

        # reply to the user by sms
        message = "Hi " + config.callers[str(from_number)] + "! Got it, " + str(todays_weight) + " today."
        twilio_response = create_sms(message)
        if DEBUG: print "* SMS ready"

        # post info to fitbit
        weight_info = {'weight' : to_kg(todays_weight), 'date' : mydate}
        params = urllib.urlencode(weight_info)
        url = '/1/user/-/body/log/weight.xml'
        apiCall = url + '?' + params
        if DEBUG: print "* submitting to url " + apiCall

        # access protected resource
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=access_token, http_url=apiCall)
        oauth_request.sign_request(signature_method, consumer, access_token)
        headers = oauth_request.to_header(realm='api.fitbit.com')
        connection.request('POST', apiCall, headers=headers)
        fitbitresp = connection.getresponse()
        xml = fitbitresp.read()
        print "* SUCCESS! Data logged at Fitbit: " + xml

    elif from_number not in config.callers:
        message = "Sorry, you can't update Fitbit from this number: " + str(from_number)
        twilio_response = create_sms(message)

    else:
        message = "Nice try buddy. That wasn't a valid number."
        twilio_response = create_sms(message)

    if DEBUG: print "* Sending SMS"
    return str(twilio_response)

if __name__ == "__main__":
    # Use Heroku's PORT variable, if available, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

