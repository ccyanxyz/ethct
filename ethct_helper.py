from constants import *

def sendtx(web3, to, value, nonce = None, data = "", show = True):
    account = web3.eth.account.privateKeyToAccount(PRIVATE_KEY)
    signed = web3.eth.account.signTransaction({
        'gasPrice': web3.toWei('21', 'gwei'),
        'gas': 1000000,
        'to': web3.toChecksumAddress(to),
        'value': web3.toWei(str(value), 'ether'),
        'nonce': nonce if nonce is not None else web3.eth.getTransactionCount(account.address),
        'data': data.encode(),
        }, account.privateKey)
    txhash = web3.eth.sendRawTransaction(signed.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(txhash)
    if show:
        print(receipt)
    return receipt

