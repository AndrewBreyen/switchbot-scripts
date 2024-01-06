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

# construct signature and nonce
t = str(int(time.time() * 1000))
nonce = "requestID"
data = TOKEN + t + nonce
sign_term = hmac.new(SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
sign = base64.b64encode(sign_term).decode('utf-8').strip()


# construct body of request
body = json.dumps({
    "command": "turnOn",
    "parameter": "default",
    "commandType": "command"
})

device_id = "MAC"

headers = {
    "Authorization": TOKEN,
    "sign": sign,
    "nonce": nonce,
    "t": t,
    'Content-Type': 'application/json',
    'Content-Length': len(body),
}

conn = http.client.HTTPSConnection("api.switch-bot.com", port=443)

conn.request("GET", f"/v1.1/devices/", body, headers)
# conn.request("POST", f"/v1.1/devices/{device_id}/commands", body, headers)

res = conn.getresponse()
print(f"statusCode: {res.status}")
data = res.read()
print(data.decode('utf-8'))
conn.close()
