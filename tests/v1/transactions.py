#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/transactions.py
# VERSION: 	 1.0
# CREATED: 	 2021-09-27 14:25
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from decimal import Decimal
from typing import List
### Project Contracts ###
from brownie import flexUSDImplV1
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

def test_transfer_to_users(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV1):
  print(f'{ BLUE }Trasaction Test #1: Distribute 100 each to user accounts.{ NFMT }')
  amount: int = 100
  flex_usd: flexUSDImplV1 = wrap_flexusd
  for i, user_account in enumerate(user_accounts):
    amount_wei: int = Wei(f'{amount} ether').to('wei')
    txn = flex_usd.transfer(user_account, amount_wei, {'from': admin})
    print(f'Transaction #{i + 1}: ' \
      f'(from={ admin.address[:20] }..., ' \
        f'to={ user_account.address[:20] }..., ' \
          f'amount={ amount }, id={ txn.txid[:20] }... ' \
        ')')
  spent: int     = len(user_accounts) * amount
  spent_wei: int = Wei(f'{spent} ether').to('wei')
  assert flex_usd.balanceOf(admin) == (flex_usd.totalSupply() - spent_wei)

def test_transfer_while_broke(user_accounts: List[Account], wrap_flexusd: flexUSDImplV1):
  print(f'{ BLUE }Transaction Test #2: Test create failed transaction because balance insufficient.{ NFMT }')
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSDImplV1 = wrap_flexusd
  test_acct: Account      = user_accounts[0]
  target_acct: Account    = user_accounts[1]
  revert: bool            = False
  revert_msg: str
  try:
    flex_usd.transfer(target_acct, amount_wei, { 'from': test_acct })
  except VirtualMachineError as err:
    revert = True
    revert_msg = err.message
  assert revert     == True
  print(revert_msg)
  assert revert_msg == 'VM Exception while processing transaction: revert ERC20: transfer internalAmt exceeds balance'

def test_transfer_hot_potato(admin: Account, user_accounts: List[Account], wrap_flexusd: flexUSDImplV1):
  print(f'{ BLUE }Transaction Test #3: Pass the same amount around list of user accounts.{ NFMT }')
  amount: int             = 100
  amount_wei: Decimal     = Wei(f'{amount} ether').to('wei')
  flex_usd: flexUSDImplV1 = wrap_flexusd
  ### First Transfer from Admin ###
  txn: TransactionReceipt = flex_usd.transfer(user_accounts[0], amount_wei, { 'from': admin })
  print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={admin.address[:15]}..., to={user_accounts[0].address[:15]}...)>')
  assert flex_usd.balanceOf(user_accounts[0]) == amount_wei
  count: int = len(user_accounts)
  ### Pass the Hot Potato ###
  for i in range(count):
    if i >= count - 1: break
    from_addr: str = user_accounts[i]
    to_addr: str   = user_accounts[i+1]
    txn = flex_usd.transfer(to_addr, amount_wei, { 'from': from_addr })
    print(f'<Transaction (amount={amount}, txid={txn.txid[:15]}..., from={from_addr.address[:15]}..., to={to_addr.address[:15]}...)>')
    assert flex_usd.balanceOf(from_addr) == 0
    assert flex_usd.balanceOf(to_addr)   == amount_wei
