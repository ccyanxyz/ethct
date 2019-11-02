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
   ethct --compile <CONTRACT_FILE> --save
   ```

3. Deploy a contract on ropsten testnet:

   ```
   ethct --deploy <CONTRACT_FILE> --network <NETWORK> --contract <CONTRACT_NAME> --args '<PARAMETER0> <PARAMETER1> ...' --value <VALUE_IN_ETHER>
   ```

4. Call contract function:

   ```
   ethct --address <ADDRESS> --abi <ABI_FILE> --call '<FUNCTION_NAME> <PARAMETER0> <PARAMETER1> ...'
   ```

   If it's a payable function:

   ```
   ethct --address <ADDRESS> --abi <ABI_FILE> --call '<FUNCTION_NAME> <PARAMETER0> <PARAMETER1> ... value:<VALUE_IN_ETHER>'
   ```

   If the ABI file can be found in the current 'build' directory, just give the contract name:

   ```
   ethct --address <ADDRESS> --contract <CONTRACT_NAME> --call '<FUNCTION_NAME> <PARAMETER0> <PARAMETER1> ...'
   ```

5. Send raw transaction:

   ```
   ethct --sendtx --to <ADDRESS> --value <VALUE_IN_ETHER> --data <DATA> --nonce <NONCE>
   ```

6. Get contract storage:

   ```
   ethct --getstorage <ADDRESS> --position <INDEX>
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

10. Get nonce:

   ```
   ethct --getnonce <ADDRESS>
   ```

#### Example

Here is an example on how to use ethct, the contract is from [Fuzzy Identity Challenge](https://capturetheether.com/challenges/accounts/fuzzy-identity/).

Here is the challenge contract, your task is to set `isComplete` to `true`:

```js
pragma solidity ^0.4.21;

interface IName {
    function name() external view returns (bytes32);
}

contract FuzzyIdentityChallenge {
    bool public isComplete;

    function authenticate() public {
        require(isSmarx(msg.sender));
        require(isBadCode(msg.sender));

        isComplete = true;
    }

    function isSmarx(address addr) internal view returns (bool) {
        return IName(addr).name() == bytes32("smarx");
    }

    function isBadCode(address _addr) internal pure returns (bool) {
        bytes20 addr = bytes20(_addr);
        bytes20 id = hex"000000000000000000000000000000000badc0de";
        bytes20 mask = hex"000000000000000000000000000000000fffffff";

        for (uint256 i = 0; i < 34; i++) {
            if (addr & mask == id) {
                return true;
            }
            mask <<= 4;
            id <<= 4;
        }

        return false;
    }
}
```

The only way to set `isComplete` to `true` is call the `authenticate` function, but with 2 restrictions:

* The caller has to implement the `IName` interface, which means the caller has to be a contract.
* The address of the caller must contains `badc0de`, we know that contract addresses are generated deterministically in Ethereum with the rightmost 160 bits of the keccak256 result of the sender address and nonce in RLP encoding. After a while of brute forcing, we can get a right private key and nonce. [Code](https://github.com/ccyanxyz/capturetheether/blob/master/fuzzy_identity.js).

Here is our exploit contract:

```js
pragma solidity ^0.4.21;

import "./fuzzy_identity.sol";

/*
interface IName {
	function name() external view returns (string) {}
}
*/

contract returnSmarx is IName {
	function name() public view returns (bytes32) {
		return bytes32("smarx");
	}

	function exploit(address _addr) public {
		FuzzyIdentityChallenge c = FuzzyIdentityChallenge(_addr);
		c.authenticate();
	}
}

contract returnAddress {
	function keccakHash(address _addr, uint8 nonce) public returns (address) {
		return address(keccak256(0xd6, 0x94, _addr, nonce));
	}
}
```

We now have a private key `ca96819b848883b0694c8b284d55f1259849339e477e7d606f07ce0656fbe357` and a nonce value `6`,  the associate address is `0xe09FBEFc7FfE44FB5E825Edd797dE0160e1d7B3B`, we need to use this account to deploy the exploit contract and call the `exploit` funtion.

First, configure ethct with one of your own private keys:

```
ethct --config --privkey <YOUR_PRIVATE_KEY>
```

Transfer some ether to `0xe09FBEFc7FfE44FB5E825Edd797dE0160e1d7B3B`

```
ethct --sendtx --to 0xe09FBEFc7FfE44FB5E825Edd797dE0160e1d7B3B --value 0.1
```

Now switch account:

```
ethct --config --privkey ca96819b848883b0694c8b284d55f1259849339e477e7d606f07ce0656fbe357
```

Deploy `returnSmarx` contract:

```
ethct --deploy ./fuzzy_identity_solver.sol --contract returnSmarx
```

Note that the nonce should be `6` to generate the correct contract address, you can just deploy the contract 6 times, and you can check the nonce of the address use the following command:

```
ethct --getnonce 0xe09FBEFc7FfE44FB5E825Edd797dE0160e1d7B3B
```

Now we have successfully deployed the `returnSmarx` contract to address `0x433F86192F11A521261BAdC0dec67bf812360442` which contains `badc0de`.

Call the `exploit` function of `returnSmarx` contract at `0x433F86192F11A521261BAdC0dec67bf812360442`:

```
ethct --address 0x433F86192F11A521261BAdC0dec67bf812360442 --contract returnSmarx --call 'exploit 0xC56B60E8e91Dc1Bdf6231fb942cdbf5EAE74033C'
```

Or you can do it like this:

```
ethct --address 0x433F86192F11A521261BAdC0dec67bf812360442 --abi ./build/returnSmarx.abi --call 'exploit 0xC56B60E8e91Dc1Bdf6231fb942cdbf5EAE74033C'
```

Now we can check if  `isComplete` is set to `true` in the challenge contract at `0xC56B60E8e91Dc1Bdf6231fb942cdbf5EAE74033C`:

```
ethct --getstorage 0xC56B60E8e91Dc1Bdf6231fb942cdbf5EAE74033C --position 0
# result: 0x0000000000000000000000000000000000000000000000000000000000000001
```

And that's it, we just completed the Fuzzy Identity Challenge!

### 4. Why build this

To make my life easier completing the [CaptureTheEther](https://capturetheether.com) challenges.

![leaderboard](./imgs/leaderboard.png)

<div style="text-align: center">
<img src="./imgs/happynerd.gif"/>
</div>