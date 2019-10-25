import os
import json

default_config_path = os.environ['HOME'] + '/.ethct.json'

key = json.load(open(default_config_path))

URL = {
    'mainnet': "https://mainnet.infura.io/v3/" + key['infurakey'],
    'ropsten': "https://ropsten.infura.io/v3/" + key['infurakey'],
    'rinkeby': "https://rinkeby.infura.io/v3/" + key['infurakey'],
    'kovan': "https://kovan.infura.io/v3/" + key['infurakey'],
    'local': "http://localhost:8085",
}

PRIVATE_KEY = key['privkey']
