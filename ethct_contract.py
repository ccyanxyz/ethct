import os
import json
import subprocess
from constants import *
from web3 import Web3, HTTPProvider

class Contract:

    def __init__(self,
            sourcefile = None,
            abifile = None,
            bytecodefile = None,
            address = None,
            provider_url = None):
        if sourcefile is not None:
            self.sourcefile = sourcefile
        if provider_url is not None:
            self.provider_url = provider_url
        else:
            self.provider_url = URL['ropsten']
        self.web3 = Web3(HTTPProvider(self.provider_url))
        self.account = self.web3.eth.account.privateKeyToAccount(PRIVATE_KEY)
        self.web3.eth.defaultAccount = self.account

        if abifile is not None:
            self.abi = json.load(open(abifile))
        if bytecodefile is not None:
            self.bytecode = open(bytecodefile).read()
        if address is not None:
            self.address = address
        if hasattr(self, 'abi') and hasattr(self, 'address'):
            self.contract = self.web3.eth.contract(self.address, abi = self.abi)

    def compile(self, save = True):
        if hasattr(self, 'abi') and hasattr(self, 'bytecode'):
            print('contract has been compiled')
            return
        with open(self.sourcefile, 'r') as f:
            source = f.read()
            cmd = 'solc ' + self.sourcefile + ' --abi --bin -o ' + os.getcwd() + '/build --overwrite'
            subprocess.call(cmd, shell = True)
        abifile = ''
        bytecodefile = ''
        for f in os.listdir(os.getcwd() + '/build'):
            if 'abi' in f:
                abifile = f
            if 'bin' in f:
                bytecodefile = f
        self.abi = json.load(open(os.getcwd() + '/build/' + abifile))
        self.bytecode = open(os.getcwd() + '/build/' + bytecodefile).read()
        if not save:
            cmd = "rm -rf build"
            subprocess.call(cmd, shell = True)

    def deploy(self, overwrite = False):
        if hasattr(self, 'address') and not overwrite:
            print('contract has been deployed')
            return
        if not hasattr(self, 'abi') or not hasattr(self, 'bytecode'):
            self.compile(save = False)

        deploy_tx = self.web3.eth.contract(abi = self.abi, bytecode = self.bytecode).constructor().buildTransaction({
            'from': self.account.address,
            'nonce': self.web3.eth.getTransactionCount(self.account.address),
            # 'gas': 21000,
            'gasPrice': self.web3.toWei('21', 'gwei'),
            })
        signed = self.web3.eth.account.signTransaction(deploy_tx, self.account.privateKey)
        txhash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        receipt = self.web3.eth.waitForTransactionReceipt(txhash)
        self.address = receipt['contractAddress']
        print('contract address:', self.address)
        print('receipt:', receipt)

    def call(self, func_name, arg_list):
        abiinfo = {}
        for info in self.abi:
            if info['name'] == func_name:
                abiinfo = info
                break
        func = self.contract.functions.__getitem__(func_name)
        for i in range(len(abiinfo['inputs'])):
            if abiinfo['inputs'][i]['type'] == 'bytes32':
                arg_list[i] = str(arg_list[i]).encode()
            if abiinfo['inputs'][i]['type'] == 'address':
                arg_list[i] = self.web3.toChecksumAddress(arg_list[i])
        if abiinfo['constant']:
            result = func(*arg_list).call({'from': self.account.address}) 
            if isinstance(result, bytes):
                result = result.decode()
            print(result)
        else:
            tx = func(*arg_list).buildTransaction({
                'from': self.account.address,
                'nonce': self.web3.eth.getTransactionCount(self.account.address),
                'gasPrice': self.web3.toWei('21', 'gwei'),
                })
            signed = self.web3.eth.account.signTransaction(tx, self.account.privateKey)
            txhash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            receipt = self.web3.eth.waitForTransactionReceipt(txhash)
            print(receipt)

