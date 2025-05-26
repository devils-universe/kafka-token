// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Kafka is ERC20, Ownable {
    constructor() ERC20("Kafka", "KAFKA") {
        _mint(msg.sender, 1_000_000_000_000_000_000_000_000 * 10 ** decimals());
    }
}
