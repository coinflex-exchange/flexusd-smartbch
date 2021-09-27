#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/balances.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-20 14:45
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import List
### Third-Party Packages ###
from brownie.convert import Wei
from eth_account import Account
### Local Modules ###
from . import *
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
GREEN: str = '\033[1;32m'
NFMT: str  = '\033[0;0m'

def test_show_balances(admin: Account, user_accounts: List[Account]):
  print(f'{ BLUE }Account Test #1: Show accounts and assure Accounts have funds.{ NFMT }')
  starting_fund: int = Wei('100 ether').to('wei')
  assert admin.balance() == starting_fund
  print(f'Admin: { admin } { GREEN }(balance={ admin.balance() }){ NFMT }')
  for i, user_account in enumerate(user_accounts):
    assert user_account.balance() == starting_fund
    print(f'User #{i + 1}: { user_account } { GREEN }(balance={ user_account.balance() }){ NFMT }')
