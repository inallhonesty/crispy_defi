// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GGWPToken is ERC20 {
    constructor() ERC20("GGWP Token", "GGWP") {
        _mint(msg.sender, 1 * 10 ** 6 * 10 ** 18); //1 mil tokens, 18 decimals
    }
}
