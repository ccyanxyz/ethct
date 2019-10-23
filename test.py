from ethct_contract import *

contract = Contract("./test.sol")
contract.compile(save = True)

contract.deploy()
