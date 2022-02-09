#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v2/blacklist.py
# VERSION: 	 1.0
# CREATED: 	 
# AUTHOR: 	 
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from decimal import Decimal
from typing import List
### Project Contracts ###
from brownie import FlexUSDImplV2
### Third-Party Packages ###
from brownie.convert import Wei
from brownie.exceptions import VirtualMachineError
from brownie.network.transaction import TransactionReceipt
from eth_account import Account
### Local Modules ###
from tests import ( admin, user_accounts )
from . import ( deploy_impl, deploy_flexusd, wrap_flexusd )
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

def test_transfer_while_blacklisted(admin: Account, user_accounts: List[Account], wrap_flexusd: FlexUSDImplV2):
  print(f'{ BLUE }Blacklist Test #1: Transfer amount to account, blacklist it and observe failed transaction due to blacklist.{ NFMT }')
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: FlexUSDImplV2 = wrap_flexusd
  ### First Transfer from Admin ###
  from_addr: str          = admin.address
  to_addr: str            = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr[:15]}..., to={to_addr[:15]}...)>')
  assert flex_usd.balanceOf(user_accounts[0]) == amount_wei
  ### Blacklist ###
  blacklist_target: str   = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.addToBlacklist(blacklist_target, { 'from': admin })
  print(txn)
  assert txn.events['TokenBlacklist'] is not None
  print(txn.events)
  ### Try Transferring Forward ###
  from_addr: str = user_accounts[0].address
  to_addr: str   = user_accounts[1].address
  revert: bool   = False
  revert_msg: str
  try:
    flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert                        == True
  assert revert_msg                    == 'VM Exception while processing transaction: revert account is blacklisted'
  assert flex_usd.balanceOf(from_addr) == amount_wei # Balance Unchanged

def test_transfer_after_unblacklisted(admin: Account, user_accounts: List[Account], wrap_flexusd: FlexUSDImplV2):
  print(f'{ BLUE }Blacklist Test #2: Transfer amount to account, blacklist and unblacklist then transfer amount back.{ NFMT }')
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: FlexUSDImplV2 = wrap_flexusd
  ### First Transfer from Admin ###
  from_addr: str          = admin.address
  to_addr: str            = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr[:15]}..., to={to_addr[:15]}...)>')
  assert flex_usd.balanceOf(user_accounts[0]) == amount_wei
  ### Blacklist ###
  blacklist_target: str   = user_accounts[0].address
  txn: TransactionReceipt = flex_usd.addToBlacklist(blacklist_target, { 'from': admin })
  print(txn)
  assert txn.events['TokenBlacklist'] is not None
  print(txn.events)
  ### Unblacklist ###
  txn: TransactionReceipt = flex_usd.removeFromBlacklist(blacklist_target, { 'from': admin })
  print(txn)
  assert txn.events['TokenBlacklist'] is not None
  print(txn.events)
  ### First Transfer from Admin ###
  from_addr: str          = user_accounts[0].address
  to_addr: str            = admin.address
  txn: TransactionReceipt = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr[:15]}..., to={to_addr[:15]}...)>')
  assert flex_usd.balanceOf(from_addr) == 0
