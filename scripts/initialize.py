#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  initialize_flexusd.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-19 16:07
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from brownie import accounts, network, FlexUSDImplV0, Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
from eth_account.account import ValidationError
from yaml import safe_load

TERM_RED  = '\033[1;31m'
TERM_NFMT = '\033[0;0m'

def main(target: str, total_supply: int):
  ### Load Account to use ###
  acct = None
  chain = network.Chain()
  print(f'Network Chain-ID: { chain }')
  chain_map = {
    1: None,              # mainnet
    42: 'kovan',          # kovan testnet
    1337: 'dev',          # local ganache-cli evm
    10001: 'smartbch-t1a' # smartbch testnet
  }
  if chain._chainid in (1, 42, 1337, 10001):
    chain_name = chain_map[chain._chainid]
    file_name = 'wallet.yml' if chain_name is None else f'wallet.{chain_name}.yml'
    ### Load Mnemonic from YAML File ###
    try:
      with open(file_name) as f:
        content = safe_load(f)
        ### Read Mnemonic ###
        # mnemonic = content.get('mnemonic', None)
        # acct = accounts.from_mnemonic(mnemonic, count=1)
        ### Read Privkey ###
        privkey = content.get('privkey', None)
        acct = accounts.add(privkey)
    except FileNotFoundError:
      print(f'{TERM_RED}Cannot find wallet mnemonic file defined at `{file_name}`.{TERM_NFMT}')
      return
    except ValidationError:
      print(f'{TERM_RED}Invalid address found in wallet mnemonic file.{TERM_NFMT}')
      return
    ### Transfers some Ether for usage to dev wallet ###
    if chain._chainid == 1337: 
      try:
        accounts[0].transfer(acct, Wei('100 ether').to('wei'))
      except ValueError: pass
  else:
    print('!! Invalid chainid found.')
    return
  print(f'Account: {acct}')
  balance = acct.balance()
  print(f'Account Balance: {balance}')
  if balance == 0:
    return # If balance is zero, exits

  ### Set Gas Price ##
  gas_station = {
    'fast': 0.000000097,
    'standard': 0.000000085
  }
  gas_price = gas_station['standard']

  ### Initialize ###
  total_supply_wei = Wei(f'{total_supply} ether').to('wei')
  flex_impl: FlexUSDImplV0
  try:
    flex_impl = FlexUSDImplV0.at(target)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': FlexUSDImplV0.abi, 'contractName': 'FlexUSDImplV0' }
    flex_impl        = ProjectContract(project, build=build, address=target)

  limit = flex_impl.initialize.estimate_gas(total_supply_wei, { 'from': acct }) * gas_price
  txn   = flex_impl.initialize(total_supply_wei, { 'from': acct, 'gas_limit': limit })
  print(f'Initialized: { txn }')
