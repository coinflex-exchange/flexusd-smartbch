// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import './../Ownable.sol';

/**
 * Storage Abstract Contract, do not change
 */
abstract contract flexUSDStorage is Ownable {
  /**
   * Member Variable(s)
   */
  bool public initialized;

  mapping(address => uint256) internal _balances;
  mapping(address => mapping(address => uint256)) internal _allowances;
  mapping(address => bool) public blacklist;
  uint256 internal _totalSupply;
  string public constant name   = 'flexUSD';
  string public constant symbol = 'flexUSD';
  uint256 public multiplier;
  uint8 public constant decimals = 18;
  uint256 internal constant deci = 1e18;
  bool internal getpause;
}