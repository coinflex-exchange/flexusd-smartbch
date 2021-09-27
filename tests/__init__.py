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
### Local Modules ###
from .v0 import deploy_impl as deploy_impl_v0

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

@fixture
def deploy_flexusd(admin: Account, deploy_impl_v0: flexUSDImplV0) -> flexUSD:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  impl_contract: flexUSDImplV0 = deploy_impl_v0
  ### Deploy ###
  total_supply: int            = 1000000
  init_bytes: bytes            = impl_contract.initialize.encode_input(Wei(f'{total_supply} ether').to('wei'))
  flex_usd: flexUSD            = flexUSD.deploy(impl_contract, init_bytes, {'from': admin})
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
  return flex_impl

__all__ = [
  'admin', 'user_accounts',
  'deploy_flexusd', 'wrap_flexusd_v0'
]