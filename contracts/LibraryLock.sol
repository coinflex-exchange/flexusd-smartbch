// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import './FlexUSDStorage.sol';

contract LibraryLock is FlexUSDStorage {
  // Ensures no one can manipulate the Logic Contract once it is deployed.
  // PARITY WALLET HACK PREVENTION

  modifier delegatedOnly()
  {
    require(initialized, "The library is locked. No direct 'call' is allowed.");
    _;
  }

  function initialize()
    internal
  {
    initialized = true;
  }
}
