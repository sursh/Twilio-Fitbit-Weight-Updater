#!/usr/bin/env python

'''
Adapted from 
https://groups.google.com/d/topic/fitbit-api/CkXQ6-0-vMs/discussion
'''

import os, httplib
import urllib
import urllib2
from oauth import oauth
from credentials import CONSUMER_KEY, CONSUMER_SECRET

SERVER = 'api.fitbit.com'
REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % SERVER
ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % SERVER
AUTHORIZATION_URL = 'http://%s/oauth/authorize' % SERVER

ACCESS_TOKEN_STRING_FNAME = 'access_token.string'
DEBUG = False

# pass oauth request to server (use httplib.connection passed in as param)
# return response as a string
def fetch_response(oauth_request, connection, debug=DEBUG):
	url= oauth_request.to_url()
	connection.request(oauth_request.http_method,url)
	response = connection.getresponse()
	s=response.read()
	if debug:
		print 'requested URL: %s' % url
		print 'server response: %s' % s
	return s

def main():
	connection = httplib.HTTPSConnection(SERVER)
	consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
	# Fitbit API doesn't accept hmac-sha1; use plain text
	#signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
	signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()

	# if we don't have a cached access-token stored in a file, then get one
	if not os.path.exists(ACCESS_TOKEN_STRING_FNAME):

		print '* Obtain a request token ...'
		oauth_request = oauth.OAuthRequest.from_consumer_and_token(
				consumer, http_url=REQUEST_TOKEN_URL)
		if DEBUG:
			connection.set_debuglevel(10)
		oauth_request.sign_request(signature_method, consumer, None)
		resp=fetch_response(oauth_request, connection)
		auth_token=oauth.OAuthToken.from_string(resp)
		print 'Auth key: %s' % str(auth_token.key)
		print 'Auth secret: %s' % str(auth_token.secret)
		print '-'*75,'\n\n'

		# authorize the request token
		print '* Authorize the request token ...'
		auth_url="%s?oauth_token=%s" % (AUTHORIZATION_URL, auth_token.key)
		print 'Authorization URL:\n%s' % auth_url
		oauth_verifier = raw_input(
			'Please go to the above URL and authorize the '+
			'app -- Type in the Verification code from the website, when done: ')
		print '* Obtain an access token ...'
		# note that the token we're passing to the new 
		# OAuthRequest is our current request token
		oauth_request = oauth.OAuthRequest.from_consumer_and_token(
			consumer, token=auth_token, http_url=ACCESS_TOKEN_URL,
			parameters={'oauth_verifier': oauth_verifier})
		oauth_request.sign_request(signature_method, consumer, auth_token)

		# now the token we get back is an access token
		# parse the response into an OAuthToken object
		access_token=oauth.OAuthToken.from_string(
			fetch_response(oauth_request,connection))
		print 'Access key: %s' % str(access_token.key)
		print 'Access secret: %s' % str(access_token.secret)
		print '-'*75,'\n\n'


		# write the access token to file; next time we just read it from file
		if DEBUG:
			print 'Writing file', ACCESS_TOKEN_STRING_FNAME
		fobj = open(ACCESS_TOKEN_STRING_FNAME, 'w')
		access_token_string = access_token.to_string()
		fobj.write(access_token_string)
		fobj.close()

	else:
		if DEBUG:
			print 'Reading file', ACCESS_TOKEN_STRING_FNAME
		fobj = open(ACCESS_TOKEN_STRING_FNAME)
		access_token_string = fobj.read()
		fobj.close()

		access_token = oauth.OAuthToken.from_string(access_token_string)


	''' 
	Now you can access protected resources using these credentials!
	'''

	
if __name__ == '__main__':
	main()
















