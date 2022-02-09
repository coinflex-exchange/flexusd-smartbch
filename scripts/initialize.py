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
from brownie import accounts, network, FlexUSDImplV2, Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
from eth_account.account import ValidationError
from brownie.network.gas.strategies import ExponentialScalingStrategy
from yaml import safe_load


TERM_RED  = '\033[1;31m'
TERM_NFMT = '\033[0;0m'

def main(target: str="0xA9bB3b5334347F9a56bebb3f590E8dF97fC091f9", total_supply: int=1000):
  ### Load Account to use ###
  acct = None
  chain = network.Chain()
  print(f'Network Chain-ID: { chain }')
  chain_map = {
    1: None,              # mainnet
    42: 'kovan',          # kovan testnet
    1337: 'dev',          # local ganache-cli evm
    10001: 'smartbch-testnet', # smartbch testnet
    10000: 'smartbch-mainnet', # smartbch mainnet
  }
  if chain._chainid in (1, 42, 1337, 10001,10000):
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
  gas_strategy = ExponentialScalingStrategy('10 gwei', '50 gwei')
  
  ### Initialize ###
  total_supply_wei = Wei(f'{total_supply} ether').to('wei')
  flex_impl: FlexUSDImplV2
  try:
    flex_impl = FlexUSDImplV2.at(target)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': FlexUSDImplV2.abi, 'contractName': 'FlexUSDImplV2' }
    flex_impl        = ProjectContract(project, build=build, address=target)

  txn   = flex_impl.initialize(total_supply_wei, { 'from': acct, 'gas_price': gas_strategy})
  print(f'Initialized: { txn }')


