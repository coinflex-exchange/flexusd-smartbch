#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v0/approvals.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-25 12:55
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from decimal import Decimal
from typing import List
### Project Contracts ###
from brownie import flexUSDImplV0
### Third-Party Packages ###
from brownie.convert import Wei
from brownie.exceptions import VirtualMachineError
from eth_account import Account
### Local Modules ###
from tests import ( admin, user_accounts )
from . import ( deploy_impl, deploy_flexusd, wrap_flexusd )
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

def test_approve_small_amount(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV0):
  print(f'{ BLUE }Approval Test #1: Admin Approves User #1 small amount.{ NFMT }')
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSDImplV0 = wrap_flexusd
  test_account: Account   = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_full_balance(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV0):
  print(f'{ BLUE }Approval Test #2: Admin Approves User #1 full balance of admin account.{ NFMT }')
  flex_usd: flexUSDImplV0 = wrap_flexusd
  amount_wei: int         = flex_usd.balanceOf(admin)
  test_account: Account   = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_max(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV0):
  print(f'{ BLUE }Approval Test #3: Admin Approves User #1 exactly at maximum approval amount of uint256.{ NFMT }')
  amount_wei: Decimal     = Wei('115792089237316195423570985008687907853269984665640564039457 wei')
  flex_usd: flexUSDImplV0 = wrap_flexusd
  test_account: Account   = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_wei

def test_approve_above_max(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV0):
  print(f'{ BLUE }Approval Test #4: Admin Approves User #1 above maximum approval of uint256.{ NFMT }')
  amount_max: Decimal     = Wei('115792089237316195423570985008687907853269984665640564039457 wei')
  amount_wei: Decimal     = Wei('115792089237316195423570985008687907853269984665640564039458 wei')
  flex_usd: flexUSDImplV0 = wrap_flexusd
  test_account: Account   = user_accounts[0]
  flex_usd.approve(test_account, amount_wei, {'from': admin})
  assert flex_usd.allowance(admin, test_account) == amount_max

def test_approve_overflow(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV0):
  print(f'{ BLUE }Approval Test #5: Admin Approves User #1 above maximum approval of uint256.{ NFMT }')
  amount_wei: Decimal     = Wei('115792089237316195423570985008687907853269984665640564039457584007913129639935 wei')
  flex_usd: flexUSDImplV0 = wrap_flexusd
  test_account: Account   = user_accounts[0]
  revert: bool            = False
  revert_msg: str
  try:
    flex_usd.approve(test_account, amount_wei, {'from': admin})
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert == True
  assert revert_msg == 'VM Exception while processing transaction: revert'
  assert flex_usd.allowance(admin, test_account) == 0