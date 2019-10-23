import argparse
from constants import *
from ethct_contract import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compile', help = "compile contract")
    parser.add_argument('-s', '--save', help = "save compile output", action = 'store_true', default = False)
    parser.add_argument('-d', '--deploy', help = "deploy contract")
    parser.add_argument('-n', '--network', help = "choose network", default = "ropsten")
    parser.add_argument('--call', help = "call contract function")
    parser.add_argument('--address', help = "contract address")
    parser.add_argument('--abi', help = "contract ABI file")

    args = parser.parse_args()
    print(args)
    if args.compile:
        contract = Contract(args.compile)
        contract.compile(save = args.save)
    if args.deploy:
        contract = Contract(args.deploy, provider_url = URL[args.network])
        contract.deploy()

