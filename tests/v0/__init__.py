#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v0/__init__.py
# VERSION: 	 1.0
# CREATED: 	 2021-09-27 10:52
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import flexUSDImplV0
### Third-Party Packages ###
from brownie.convert import Wei
from eth_account import Account
from pytest import fixture
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

@fixture
def deploy_impl(admin: Account) -> flexUSDImplV0:
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

__all__ = [
  'deploy_impl', 'deploy_impl_clone'
]