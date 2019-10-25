import json

key = json.load(open('config.json'))

URL = {
    'mainnet': "https://mainnet.infura.io/v3/" + key['infura_key'],
    'ropsten': "https://ropsten.infura.io/v3/" + key['infura_key'],
    'rinkeby': "https://rinkeby.infura.io/v3/" + key['infura_key'],
    'kovan': "https://kovan.infura.io/v3/" + key['infura_key'],
    'local': "http://localhost:8085",
}

PRIVATE_KEY = key['privkey']
