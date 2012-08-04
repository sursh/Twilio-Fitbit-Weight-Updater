Twilio-Fitbit integration

Sasha Laundy, 2012

This app lets you update your weight in your Fitbit profile by sending a text message. I am too cheap to buy their wireless scale for $130, and would rather pay Twilio $7.30/year.

Fitbit is a sophisticated pedometer that wirelessly syncs when you're near your base station. It updates your data to your Fitbit dashboard at fitbit.com. It's pretty cool because it helps you measure and change your activity and sleep levels. You'll need an account with them in order to use this app. 

Install dependencies as noted in app.py, noting:
 * oauth (Fitbit uses 1 NOT 2)
 * head to twilio.com/docs and download their Python library

API info: 
 * Make a Fitbit account. Create your Fitbit app.
 * Make a Twilio account. Buy an SMS-enabled (non-toll-free) phone number of your choice.

Setup:
 * Store your Fitbit consumer key and consumer secret in credentials.py
 * Update your name, phone number, and units choice in config.py

Usage: 
 * Run cl_oauth1.py on the command line to do the 3-legged handshake and authorize the app. You only need to do this once.
 * Deploy your Flask app. 
 * Configure your Twilio number to ping your app's URL when it receives a text message: paste the URL in the SMS Request URL box in your account dashboard.
 * Send SMS from your phone to your Twilio number with today's weight. 


Thanks: 

Many thanks to mikew on the Fitbit forums for sharing his oauth script: 
https://groups.google.com/forum/#!msg/fitbit-api/CkXQ6-0-vMs/VaX_V6gm3BUJ

Props to Rob Spectre for his Twilio on Flask tutorial: 
http://www.twilio.com/blog/2012/01/making-an-sms-birthday-card-with-python-and-flask.html

This explanation was very helpful for wrapping my mind around oauth: 
http://marktrapp.com/blog/2009/09/17/oauth-dummies
