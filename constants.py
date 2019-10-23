import json

URL = {
    'mainnet': "https://mainnet.infura.io/v3/bda996b482e944bdbd5bad497e8f7205",
    'ropsten': "https://ropsten.infura.io/v3/bda996b482e944bdbd5bad497e8f7205",
}

key = json.load(open('key.json'))
PRIVATE_KEY = key['privkey']
