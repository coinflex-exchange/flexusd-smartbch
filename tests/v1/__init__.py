#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v1/__init__.py
# VERSION: 	 1.0
# CREATED: 	 2021-09-27 14:25
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import flexUSD, flexUSDImplV1
### Third-Party Packages ###
from brownie.convert import Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
from eth_account import Account
from pytest import fixture
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

@fixture
def deploy_impl(admin: Account) -> flexUSDImplV1:
  '''
  Deploy and Inititialize Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V1 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: flexUSDImplV1 = flexUSDImplV1.deploy({'from': admin})
  total_supply: int       = Wei('0 ether').to('wei')
  ### Initialize ###
  flex_usd.initialize(total_supply, {'from': admin})
  return flex_usd

@fixture
def deploy_flexusd(admin: Account, deploy_impl: flexUSDImplV1) -> flexUSD:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  impl_contract: flexUSDImplV1 = deploy_impl
  ### Deploy ###
  total_supply: int            = 1000000
  init_bytes: bytes            = impl_contract.initialize.encode_input(Wei(f'{total_supply} ether').to('wei'))
  flex_usd: flexUSD            = flexUSD.deploy(impl_contract, init_bytes, {'from': admin})
  return flex_usd

@fixture
def wrap_flexusd(admin: Account, deploy_flexusd: flexUSD) -> flexUSDImplV1:
  '''
  Wrapping flexUSD address with flexUSDImplV1 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping flexUSD with Impl V1{ NFMT }')
  flex_usd: flexUSD = deploy_flexusd
  ### Wrap ###
  flex_impl: flexUSDImplV1
  try:
    flex_impl = flexUSDImplV1.at(flex_usd.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': flexUSDImplV1.abi, 'contractName': 'flexUSDImplV1' }
    flex_impl        = ProjectContract(project, build=build, address=flex_usd.address)
  return flex_impl


__all__ = [
  'deploy_impl', 'deploy_flexusd', 'wrap_flexusd'
]