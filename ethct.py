#!/usr/bin/env python
import argparse
from web3 import Web3, HTTPProvider
from constants import *
from ethct_contract import *
from ethct_helper import *

def check_config():
    with open(default_config_path, 'r') as f:
        config = json.load(f)
        if config['infurakey'] == '' and config['network'] != 'local':
            print('please config your infura apikey')
            exit()

def check_privkey():
    with open(default_config_path, 'r') as f:
        config = json.load(f)
        if len(config['accounts']) == 0:
            print('please config your private key')
            exit()
        if config['defaultAccount'] >= len(config['accounts']):
            print('please reset your defaultAccount')
            exit()
        
def main():
    parser = argparse.ArgumentParser()
    # compile contract
    parser.add_argument('-c', '--compile', help = "compile contract")
    parser.add_argument('-s', '--save', help = "save compile output", action = 'store_true', default = False)
    # deploy contract
    parser.add_argument('-d', '--deploy', help = "deploy contract")
    parser.add_argument('-n', '--network', help = "choose network")
    parser.add_argument('-v', '--value', help = "deploy tx value", default = None, type = float)
    # call contract function
    parser.add_argument('--address', help = "contract address")
    parser.add_argument('--abi', help = "contract ABI file")
    parser.add_argument('--call', help = "call contract function")
    # tools
    # get tx by hash
    parser.add_argument('--gettx', help = "get transaction info by txhash")
    # get block
    parser.add_argument('--getblock', help = "get block by hash/block_number")
    # get contract storage
    parser.add_argument('--getstorage', help = "get contract storage")
    parser.add_argument('--position', help = "contract storage position", type = int, default = 0)
    # get account balance
    parser.add_argument('--getbalance', help = "get account balance")
    # config
    parser.add_argument('--config', help = "add config options", action = "store_true")
    parser.add_argument('--privkey', help = "add private key")
    parser.add_argument('--infurakey', help = "set infura apikey")
    parser.add_argument('--account', help = "set default account", default = None)
    parser.add_argument('--delete', help = "delete account", type = int)

    parser.add_argument('--showconfig', help = "print config", action = "store_true")
    # sendtx
    parser.add_argument('--sendtx', help = "send tx", action = "store_true")
    parser.add_argument('--to', help = "tx receiver")
    parser.add_argument('--data', help = "tx data")
    parser.add_argument('--nonce', help = "tx nonce")

    args = parser.parse_args()
    network = NETWORK
    if args.network is not None:
        network = args.network
    web3 = Web3(HTTPProvider(URL[network]))
    if not args.config:
        if not os.path.exists(default_config_path):
            print('use `ethct --config --privkey <PRIVKEY> --infurakey <APIKEY> --network <NETWORK>` to config the tool first')
            exit()
        check_config()

    if args.compile:
        contract = Contract(args.compile)
        contract.compile(save = args.save)
    elif args.deploy:
        check_privkey()
        contract = Contract(args.deploy, provider_url = URL[network])
        contract.deploy(value = args.value)
    elif args.call:
        check_privkey()
        contract = Contract(abifile = args.abi, address = args.address, provider_url = URL[network])
        arg_list = args.call.split(' ')
        func_name = arg_list[0]
        contract.call(func_name, arg_list[1:])
    elif args.gettx:
        txinfo = web3.eth.getTransaction(args.gettx)
        print(txinfo)
    elif args.getblock:
        block = None
        fulltx = False
        if args.getblock in ['latest', 'earliest', 'pending']:
            block = web3.eth.getBlock('latest', full_transactions = fulltx)
        elif len(args.getblock) > 15:
            block = web3.eth.getBlock(args.getblock, full_transactions = fulltx)
        elif len(args.getblock) <= 15:
            block = web3.eth.getBlock(int(args.getblock), full_transactions = fulltx)
        print(block)
    elif args.getstorage:
        result = web3.eth.getStorageAt(args.getstorage, int(args.position))
        print(result.hex())
    elif args.getbalance:
        result = web3.eth.getBalance(web3.toChecksumAddress(args.getbalance))
        balance = web3.fromWei(result, 'ether')
        print(balance)
    elif args.config:
        config = {}
        if not os.path.exists(default_config_path):
            config = {
                    'accounts': [],
                    'defaultAccount': 0,
                    'network': 'ropsten',
                    'infurakey': '',
            }
        else:
            config = json.load(open(default_config_path, 'r'))
        if args.network:
            config['network'] = args.network
        if args.privkey:
            config['accounts'].append(args.privkey)
            config['defaultAccount'] = len(config['accounts']) - 1
        if args.infurakey:
            config['infurakey'] = args.infurakey
        if args.account is not None:
            if int(args.account) >= 0 and int(args.account) < len(config['accounts']):
                config['defaultAccount'] = int(args.account)
            else:
                print('account index out of range')
                exit()
        if args.delete:
            config['accounts'].pop(args.delete)
            config['defaultAccount'] = 0
        f = open(default_config_path, 'w')
        json.dump(config, f)
    elif args.showconfig:
        if not os.path.exists(default_config_path):
            print('config file not found')
        else:
            config = json.load(open(default_config_path))
            print(config)
    elif args.sendtx:
        if not args.value:
            print('please provide tx value with `--value` option')
            exit()
        if not args.to:
            print('please provider tx receiver with `--to` option')
            exit()
        nonce = None
        data = ""
        if args.nonce:
            nonce = int(args.nonce)
        if args.data:
            data = args.data
        sendtx(web3 = web3, to = args.to, value = args.value, nonce = nonce, data = data)

if __name__ == '__main__':
    main()
