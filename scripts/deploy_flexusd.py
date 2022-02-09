#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  deploy_flexusd.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-19 16:07
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
from brownie import accounts, network, FlexUSD, FlexUSDImplV2, Wei
from eth_account.account import ValidationError
from brownie.network.gas.strategies import ExponentialScalingStrategy
from yaml import safe_load

TERM_RED  = '\033[1;31m'
TERM_NFMT = '\033[0;0m'

def main():
  ### Load Account to use ###
  acct = None
  chain = network.Chain()
  print(f'Network Chain-ID: { chain }')
  chain_map = {
    1: None,              # mainnet
    42: 'kovan',          # kovan testnet
    1337: 'dev',          # local ganache-cli evm
    10001: 'smartbch-testnet', # smartbch testnet
    10000: 'smartbch-mainnet'  # smartbch testnet
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

  gas_strategy = ExponentialScalingStrategy('10 gwei', '50 gwei')

  ### Deployments ###
  impl_v2: FlexUSDImplV2 = FlexUSDImplV2.deploy({ 'from': acct, 'gas_price': gas_strategy })
  print(f'FlexUSDImplV2: { impl_v2 }')

  flex_usd: FlexUSD      = FlexUSD.deploy(impl_v2.address, b'', { 'from': acct, 'gas_price': gas_strategy })
  print(f'flexUSD: { flex_usd }')
