#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/__init__.py
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
from brownie.convert import  Wei
from brownie.network import accounts
from eth_account import Account
from pytest import fixture
from yaml import safe_load

### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
RED: str   = '\033[1;31m'
NFMT: str  = '\033[0;0m'

@fixture
def admin() -> Account:
  file_name: str = 'wallet.test.yml'
  ### Load Mnemonic from YAML File ###
  try:
    with open(file_name) as f:
      content = safe_load(f)
      ### Read Mnemonic ###
      mnemonic = content.get('mnemonic', None)
      acct = accounts.from_mnemonic(mnemonic, count=1)
  except FileNotFoundError:
    print(f'{ RED }Cannot find wallet mnemonic file defined at `{ file_name }`.{ NFMT }')
    return
  ### Transfer Initial Balance to Test WAllet ###
  try:
    accounts[0].transfer(acct, Wei('100 ether').to('wei'))
  except ValueError: pass
  return acct

@fixture
def user_accounts() -> List[Account]:
  '''
  Use remaining accounts set up by Ganache-cli to be list of user accounts.
  '''
  return accounts[1:10]

__all__ = [
  'admin', 'user_accounts'
]