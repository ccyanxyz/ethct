## Ethct: Ethereum contract tool (command line)

### 1. Now support:

* contract compiliation
* contract deployment
* contract function calls

### 2. E.g.

Compile a contract and save the output files:

```
./ethct.py -c test.sol -s
```

Deploy a contract on ropsten testnet:

```
./ethct.py -d test.sol -n ropsten
```

Call contract function:

```
./ethch.py --address 0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee --abi ./build/CaptureTheEther.abi --call 'setNickname ccyanxyz'
```

### 3. Why build this

To make my life easier completing the [CaptureTheEther](https://capturetheether.com) challenges.

