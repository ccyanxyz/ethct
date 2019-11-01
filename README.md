## Ethct: Ethereum contract tool (command line)

### 1. Now support:

* Contract compiliation
* Contract deployment
* Contract function calls
* Retrieve infomation from chain

### 2. Install

Install solc on MacOS:

```
brew tap ethereum/ethereum
brew install solidity
```

For Linux/Windows, please refer to the [Solidity documentation](https://solidity.readthedocs.io/en/latest/installing-solidity.html#binary-packages).

Install ethct:

```
pip install ethct
```

### 3. Usage

1. Config the tool first:

   ```
   ethct --config --privkey <PRIVKEY> --infurakey <INFURAKEY> --network <NETWORK>
   ```

2. Compile a contract and save the output files:

   ```
   ethct --compile test.sol --save
   ```

3. Deploy a contract on ropsten testnet:

   ```
   ethct --deploy test.sol --network ropsten
   ```

4. Call contract function:

   ```
   ethct --address 0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee --abi ./build/CaptureTheEther.abi --call 'setNickname ccyanxyz'
   ```

5. Call a payable function:

   ```
   ethct --address 0x2F796FaC147d6fff8b2485d05aE7FB823A478317 --abi ./build/PredictTheBlockHashChallenge.abi --call 'lockInGuess 0x0000000000000000000000000000000000000000000000000000000000000000 value:1'
   ```

   'value:1'  means the value of this transaction is 1 ether.

6. Get contract storage:

   ```
   ethct --getstorage 0x2F796FaC147d6fff8b2485d05aE7FB823A478317 --position 2
   ```

7. Get block:

   ```
   ethct --getblock <BLOCKNUM>/latest/earliest/pending/<BLOCKHASH>
   ```

8. Get transaction:

   ```
   ethct --gettx <TXHASH>
   ```

9. Get balance:

   ```
   ethct --getbalance <ADDRESS>
   ```

### 4. Why build this

To make my life easier completing the [CaptureTheEther](https://capturetheether.com) challenges.

