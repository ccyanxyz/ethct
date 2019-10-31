import os
import json

default_config_path = os.environ['HOME'] + '/.ethct.json'

try:
    config = json.load(open(default_config_path))
except:
    config = {
            'accounts':[],
            'defaultAccount': 0,
            'network': 'ropsten',
            'infurakey': '',
    }

URL = {
    'mainnet': "https://mainnet.infura.io/v3/" + config['infurakey'],
    'ropsten': "https://ropsten.infura.io/v3/" + config['infurakey'],
    'rinkeby': "https://rinkeby.infura.io/v3/" + config['infurakey'],
    'kovan': "https://kovan.infura.io/v3/" + config['infurakey'],
    'local': "http://localhost:8545",
}

NETWORK = config['network']
try:
    defaultAccount = config['defaultAccount']
    PRIVATE_KEY = config['accounts'][defaultAccount]
except:
    defaultAccount = None
    PRIVATE_KEY = None
