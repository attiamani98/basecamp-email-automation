from basecampapi import Basecamp 
import logging
import os
from dotenv import load_dotenv
import json
import requests

# Load environment variables from .env file
load_dotenv()
"""
your_credentials = {
	"account_id": os.environ["BASECAMP_ACCOUNT_ID"],
	"client_id": os.environ["BASECAMP_CLIENT_ID"],
	"client_secret": os.environ["BASECAMP_CLIENT_SECRET"],
	"redirect_uri": os.environ["BASECAMP_REDIRECT_URL"]
}
"""
# Basecamp API endpoint URLs
authorization_base_url = 'https://launchpad.37signals.com/authorization/new'
token_url = 'https://launchpad.37signals.com/authorization/token'

# Client credentials
client_id = os.environ["BASECAMP_CLIENT_ID"]
client_secret = os.environ["BASECAMP_CLIENT_SECRET"]
redirect_uri = os.environ["BASECAMP_REDIRECT_URL"]  # This should be set up in your Basecamp application settings

# Authorization parameters
params = {
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'type': 'web_server',  # Use 'web_server' for server-side applications
    'scope': 'read write'  # Adjust the scope based on the permissions your app needs
}

# Step 1: Redirect the user to the authorization URL
authorization_url = authorization_base_url + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
print("Go to the following URL and authorize access:", authorization_url)

# Step 2: After authorization, the user will be redirected to your redirect URI with an authorization code

# Extract the authorization code from the redirect URI
authorization_code = input("Enter the authorization code from the redirect URI: ")

# Step 3: Exchange the authorization code for an access token
token_data = {
    'type': 'web_server',  # Use 'web_server' for server-side applications
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'code': authorization_code
}

response = requests.post(token_url, data=token_data)
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Failed to obtain access token:", response.text)
