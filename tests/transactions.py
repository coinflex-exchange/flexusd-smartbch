#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/transactions.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-21 12:33
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import List
### Third-Party Packages ###
from brownie.network.account import Account
### Local Modules ###
from . import *
from .accounts import *
from .deployments import *

def test_show_accounts(admin: Account, user_accounts: List[Account]):
  print(f'{ BLUE }Test #1 Show accounts and assure Accounts have funds.{ NFMT }')
  starting_fund: int = Wei('100 ether').to('wei')
  assert admin.balance() == starting_fund
  print(f'Admin: { admin } { GREEN }(balance={ admin.balance() }){ NFMT }')
  for i, user_account in enumerate(user_accounts):
    assert user_account.balance() == starting_fund
    print(f'User #{i + 1}: { user_account } { GREEN }(balance={ user_account.balance() }){ NFMT }')

def test_deployments(deploy_impl_v0: FlexUSDImplV0, wrap_flexusd_v0: FlexUSDImplV0):
  print(f'{ BLUE }Test #2 Deploy Implementation Logic and then FlexUSD.{ NFMT }')
  impl_v0: FlexUSDImplV0  = deploy_impl_v0
  flex_usd: FlexUSDImplV0 = wrap_flexusd_v0
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V0: { impl_v0 } (totalSupply={ impl_v0.totalSupply() }, admin={ impl_v0.owner() })')
  print(f'FlexUSD: { flex_usd } (totalSupply={ flex_usd.totalSupply()}, admin={ flex_usd.owner() })')
  assert impl_v0.totalSupply() != flex_usd.totalSupply() # Storage is not shared, logic is;
  assert impl_v0.owner()       == flex_usd.owner()       # Initialized by the same key

def test_transfer_to_users(admin: Account, user_accounts: List[Account], wrap_flexusd_v0: FlexUSDImplV0):
  print(f'{ BLUE }Test #3 Distribute 100 each to user accounts.{ NFMT }')
  amount: int = 100
  flex_usd: FlexUSDImplV0 = wrap_flexusd_v0
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
