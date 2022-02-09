#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/V2/__init__.py
# VERSION: 	 1.0
# CREATED: 	 
# AUTHOR: 	 
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import FlexUSD, FlexUSDImplV2
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
def deploy_impl(admin: Account) -> FlexUSDImplV2:
  '''
  Deploy and Inititialize Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V2 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: FlexUSDImplV2 = FlexUSDImplV2.deploy({'from': admin})
  total_supply: int       = Wei('0 ether').to('wei')
  ### Initialize ###
  flex_usd.initialize(total_supply, {'from': admin})
  return flex_usd

@fixture
def deploy_flexusd(admin: Account, deploy_impl: FlexUSDImplV2) -> FlexUSD:
  print(f'{ BLUE }Event: flexUSD Deployment{ NFMT }')
  impl_contract: FlexUSDImplV2 = deploy_impl
  ### Deploy ###
  total_supply: int            = 1000000
  init_bytes: bytes            = impl_contract.initialize.encode_input(Wei(f'{total_supply} ether').to('wei'))
  flex_usd: FlexUSD            = FlexUSD.deploy(impl_contract, init_bytes, {'from': admin})
  return flex_usd

@fixture
def wrap_flexusd(admin: Account, deploy_flexusd: FlexUSD) -> FlexUSDImplV2:
  '''
  Wrapping flexUSD address with flexUSDImplV2 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping flexUSD with Impl V2{ NFMT }')
  flex_usd: FlexUSD = deploy_flexusd
  ### Wrap ###
  flex_impl: FlexUSDImplV2
  try:
    flex_impl = FlexUSDImplV2.at(flex_usd.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': FlexUSDImplV2.abi, 'contractName': 'FlexUSDImplV2' }
    flex_impl        = ProjectContract(project, build=build, address=flex_usd.address)
  return flex_impl


__all__ = [
  'deploy_impl', 'deploy_flexusd', 'wrap_flexusd'
]