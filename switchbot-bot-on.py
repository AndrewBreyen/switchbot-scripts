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



#URL = "/v1.1/devices/"
URL = '/v1.1/devices/ED5649D48456/commands'
METHOD = "POST"
COMMAND_BODY = json.dumps({
    "command": "turnOn",
    "parameter": "default",
    "commandType": "command"
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
print('COMMAND SENT:')
print(f"{METHOD}, {URL}, {COMMAND_BODY}, {HEADERS}")
print(f"statusCode: {res.status} {res.reason}")
