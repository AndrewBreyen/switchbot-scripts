import hashlib
import hmac
import json
import time
import http.client
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.environ['SWITCHBOT_TOKEN']
SECRET = os.environ['SWITCHBOT_SECRET']



URL = "/v1.1/devices/"
METHOD = "GET"
COMMAND_BODY = json.dumps({
    
})




# construct signature and nonce
t = str(int(time.time() * 1000))
nonce = "requestID"
data = TOKEN + t + nonce
sign_term = hmac.new(SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
sign = base64.b64encode(sign_term).decode('utf-8').strip()


HEADERS = {
    "Authorization": TOKEN,
    "sign": sign,
    "nonce": nonce,
    "t": t,
    'Content-Type': 'application/json',
    'Content-Length': len(COMMAND_BODY),
}

conn = http.client.HTTPSConnection("api.switch-bot.com", port=443)

conn.request(METHOD, URL, COMMAND_BODY, HEADERS)

res = conn.getresponse()
print(f"statusCode: {res.status}")
data = res.read()

# Pretty print the JSON response if it's not empty
if data:
    try:
        parsed_response = json.loads(data)
        pretty_response = json.dumps(parsed_response, indent=2)
        print(pretty_response)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
else:
    print("Empty response from the server.")
