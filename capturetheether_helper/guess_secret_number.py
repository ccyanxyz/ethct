from web3 import Web3

def find(hash_val):
    for i in range(0, 100000):
        if Web3.soliditySha3(['uint8'], [i]).hex() == hash_val:
            return i
    return None

if __name__ == '__main__':
    hash_val = "0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365"
    num = find(hash_val)
    if num is None:
        print('not found')
    else:
        print(num)
        # answer is 170
