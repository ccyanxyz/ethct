#!/usr/bin/env python
import argparse
from web3 import Web3, HTTPProvider
from constants import *
from ethct_contract import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # compile contract
    parser.add_argument('-c', '--compile', help = "compile contract")
    parser.add_argument('-s', '--save', help = "save compile output", action = 'store_true', default = False)
    # deploy contract
    parser.add_argument('-d', '--deploy', help = "deploy contract")
    parser.add_argument('-n', '--network', help = "choose network", default = "ropsten")
    # call contract function
    parser.add_argument('--address', help = "contract address")
    parser.add_argument('--abi', help = "contract ABI file")
    parser.add_argument('--call', help = "call contract function")
    # tools
    # get tx by hash
    parser.add_argument('--gettx', help = "get transaction info by txhash")

    args = parser.parse_args()
    if args.compile:
        contract = Contract(args.compile)
        contract.compile(save = args.save)
    elif args.deploy:
        contract = Contract(args.deploy, provider_url = URL[args.network])
        contract.deploy()
    elif args.call:
        contract = Contract(abifile = args.abi, address = args.address, provider_url = URL[args.network])
        arg_list = args.call.split(' ')
        func_name = arg_list[0]
        contract.call(func_name, arg_list[1:])
    elif args.gettx:
        web3 = Web3(HTTPProvider(URL[args.network]))
        txinfo = web3.eth.getTransaction(args.gettx)
        print(txinfo)
