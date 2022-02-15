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
from brownie import accounts, network, FlexUSD,FlexUSDImplV2, Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
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
    10001:'smartbch-testnet', # smartbch testnet
    10000:'smartbch-mainnet', # smartbch mainnet
    97:'bsc-test',            # binance smart chain testnet
    56:'bsc-main',            # binance smart chain mainnet
    4002:'ftm-test',          # fantom opera testnet
    250:'ftm-main',           # fantom opera testnet
    137:'polygon-mainnet',    # polygon mainnet
    80001:'polygon-testnet',  # (polygon) mumbai testnet
    43113:'avalanche-testnet',# avalanche testnet
    43114:'avalanche-mainnet' # avalanche mainnet
  }
  if chain._chainid in (1, 42, 1337, 10001, 10000, 97, 56, 4002, 250, 137, 80001, 43113, 43114):
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
  
  ### Loads Deployment Parameters ###

  #pp
  ppflexUSD_proxy:str = None
  ppflexUSD_impl :str = None
  ppflexUSD_owner : str = None

  #stage
  stgflexUSD_proxy:str = None
  stgflexUSD_impl:str = None
  ppflexUSD_owner: str = None

  #prod
  flexUSD_proxy: str = None
  flexUSD_impl: str = None
  flexUSD_owner: str = None
  
  #deployment phase
  deploy_on: str = None

  try:
    with open('params/params.yml', 'rb') as dep:
      params: dict = safe_load(dep)
      #pp
      ppflexUSD_proxy      = params.get('ppflexUSD_proxy', None)
      ppflexUSD_impl       = params.get('ppflexUSD_impl', None)
      ppflexUSD_owner      = params.get('ppflexUSD_owner', None)
      #stage
      stgflexUSD_proxy      = params.get('stgflexUSD_proxy', None)
      stgflexUSD_impl       = params.get('stgflexUSD_impl', None)
      stgflexUSD_owner      = params.get('stgflexUSD_owner', None)
      #prod
      flexUSD_proxy         = params.get('flexUSD_proxy', None)
      flexUSD_impl          = params.get('flexUSD_impl', None)
      flexUSD_owner         = params.get('flexUSD_owner', None)
      
      #deployment phase
      deploy_on: str = params.get('deploy_on', None)
      
      
      if ppflexUSD_proxy is None or not isinstance(ppflexUSD_proxy, str):
        print(f'{TERM_RED}Invalid `ppflexUSD_proxy` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif ppflexUSD_impl is None or not isinstance(ppflexUSD_impl, str):
        print(f'{TERM_RED}Invalid `ppflexUSD_impl` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif ppflexUSD_owner is None or not isinstance(ppflexUSD_owner, str):
        print(f'{TERM_RED}Invalid `ppflexUSD_owner` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif stgflexUSD_proxy is None or not isinstance(stgflexUSD_proxy, str):
        print(f'{TERM_RED}Invalid `stgflexUSD_proxy` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif stgflexUSD_impl is None or not isinstance(stgflexUSD_impl, str):
        print(f'{TERM_RED}Invalid `stgflexUSD_impl` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif stgflexUSD_owner is None or not isinstance(stgflexUSD_owner, str):
        print(f'{TERM_RED}Invalid `stgflexUSD_owner` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif flexUSD_proxy is None or not isinstance(flexUSD_proxy, str):
        print(f'{TERM_RED}Invalid `flexUSD_proxy` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif flexUSD_impl is None or not isinstance(flexUSD_impl, str):
        print(f'{TERM_RED}Invalid `flexUSD_impl` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif flexUSD_owner is None or not isinstance(flexUSD_owner, str):
        print(f'{TERM_RED}Invalid `flexUSD_owner` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
      elif deploy_on is None or not isinstance(deploy_on, str):
        print(f'{TERM_RED}Invalid `deploy_on` parameter found in `params/params.yml` file.{TERM_NFMT}')
        return
  except FileNotFoundError:
    print(f'{TERM_RED}Cannot find `params/params.yml` file containing deployment parameters.{TERM_NFMT}')
    return

  gas_strategy = ExponentialScalingStrategy('10 gwei', '50 gwei')

  if deploy_on == "pp":
    owner = ppflexUSD_owner;
    proxy = ppflexUSD_proxy;
    impl = ppflexUSD_impl;
  elif deploy_on == "stg":
    owner = stgflexUSD_owner;
    proxy = ppflexUSD_proxy;
    impl = ppflexUSD_impl;
  elif deploy_on == "prod":
    owner = flexUSD_owner;
    proxy = flexUSD_proxy;
    impl = flexUSD_impl;

  ### Onwership transfer ###
  FlexUSDDeployed:FlexUSD
  FlexUSDDeployed=FlexUSD.at(proxy)

  txn   = FlexUSDDeployed.transferOwnership(owner, { 'from': acct, 'gas_price': gas_strategy})
  print(f'Ownership of FlexUSD proxy transferred to : { txn }')

  ### Onwership transfer ###
  FlexUSDImplV2Deployed:FlexUSDImplV2
  FlexUSDImplV2Deployed=FlexUSDImplV2.at(impl)

  txn   = FlexUSDImplV2Deployed.transferOwnership(owner, { 'from': acct, 'gas_price': gas_strategy })
  print(f'Ownership Logic (FlexUSD) transferred to : { txn }')