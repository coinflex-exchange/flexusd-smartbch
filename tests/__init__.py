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
### Import Project Contracts ###
from brownie import flexUSD, flexUSDImplV0
### Third-Party Packages ###
from brownie.convert import  Wei
from brownie.exceptions import ContractExists
from brownie.network import accounts
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
from eth_account import Account
from pytest import fixture
from yaml import safe_load

### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
RED: str   = '\033[1;31m'
GREEN: str = '\033[1;32m'
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

@fixture
def deploy_impl_v0(admin: Account) -> flexUSDImplV0:
  '''
  Deploy and Inititialize Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V0 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: flexUSDImplV0 = flexUSDImplV0.deploy({'from': admin})
  total_supply: int       = Wei('0 ether').to('wei')
  ### Initialize ###
  flex_usd.initialize(total_supply, {'from': admin})
  return flex_usd

@fixture
def deploy_impl_clone(admin: Account) -> flexUSDImplV0:
  '''
  Deploy and Initialize Cloned Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V0 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: flexUSDImplV0 = flexUSDImplV0.deploy({'from': admin})
  total_supply: int       = Wei('0 ether').to('wei')
  ### Initialize ###
  flex_usd.initialize(total_supply, {'from': admin})
  return flex_usd

@fixture
def deploy_flexusd(admin: Account, deploy_impl_v0: flexUSDImplV0) -> flexUSD:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  impl_contract: flexUSDImplV0 = deploy_impl_v0
  ### Deploy ###
  flex_usd: flexUSD            = flexUSD.deploy(impl_contract, b'', {'from': admin})
  return flex_usd

@fixture
def wrap_flexusd_v0(admin: Account, deploy_flexusd: flexUSD) -> flexUSDImplV0:
  '''
  Wrapping flexUSD address with flexUSDImplV0 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping flexUSD with Impl V0{ NFMT }')
  flex_usd: flexUSD = deploy_flexusd
  ### Wrap ###
  flex_impl: flexUSDImplV0
  try:
    flex_impl = flexUSDImplV0.at(flex_usd.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': flexUSDImplV0.abi, 'contractName': 'flexUSDImplV0' }
    flex_impl        = ProjectContract(project, build=build, address=flex_usd.address)
  ### Initialize ###
  total_supply: int  = Wei('1000000 ether').to('wei')
  flex_impl.initialize(total_supply, {'from': admin})
  return flex_impl
