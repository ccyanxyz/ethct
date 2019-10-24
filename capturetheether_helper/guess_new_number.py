from constants import *
from ethct_contract import *
from web3 import Web3, HTTPProvider
import time

web3 = Web3(HTTPProvider(URL['ropsten']))

def get_new_number():
    block = web3.eth.getBlock(web3.eth.blockNumber)
    hash_val = web3.soliditySha3(['bytes32', 'uint8'], [block['hash'], int(time.time())]).hex()
    return int(hash_val, 16) % 256

if __name__ == '__main__':
    num = get_new_number()

    address = "0x34639021E6675c7F47940c218c957cff37f80Ed7"
    abifile = "../build/GuessTheNewNumberChallenge.abi"
    contract = Contract(address = address, abifile = abifile, provider_url = URL['ropsten'])
    arg_list = [str(num), 'value:1']
    contract.call('guess', arg_list)
