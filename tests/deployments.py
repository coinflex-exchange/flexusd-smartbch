#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/deployments.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-20 14:45
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Third-Party Packages ###
from pytest import fixture
from brownie import FlexUSD, FlexUSDImplV0, Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
### Local Modules ###
from . import *
from .accounts import *

@fixture
def deploy_impl_v0(admin: Account) -> FlexUSDImplV0:
  '''
  Deploy and Initiate Implementation Logic Contract with totalSupply of 0.
  '''
  print(f'{ BLUE }Event: FlexUSD Implementation Logic V0 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: FlexUSDImplV0 = FlexUSDImplV0.deploy({'from': admin})
  total_supply: int       = Wei('0 ether').to('wei')
  ### Initialize ###
  flex_usd.initialize(total_supply, {'from': admin})
  return flex_usd

@fixture
def deploy_flexusd(admin: Account, deploy_impl_v0: FlexUSDImplV0) -> FlexUSD:
  print(f'{ BLUE }Event: FlexUSD Deployment{ NFMT }')
  impl_contract: FlexUSDImplV0 = deploy_impl_v0
  ### Deploy ###
  flex_usd: FlexUSD            = FlexUSD.deploy(impl_contract, b'', {'from': admin})
  return flex_usd

@fixture
def wrap_flexusd_v0(admin: Account, deploy_flexusd: FlexUSD) -> FlexUSDImplV0:
  '''
  Wrapping FlexUSD address with FlexUSDImplV0 Container and Initialize with totalSupply of 1,000,000 
  '''
  print(f'{ BLUE }Event: Wrapping FlexUSD with Impl V0{ NFMT }')
  flex_usd: FlexUSD = deploy_flexusd
  ### Wrap ###
  flex_impl: FlexUSDImplV0
  try:
    flex_impl = FlexUSDImplV0.at(flex_usd.address)
  except ContractExists:
    project: Project = get_loaded_projects()[0]
    build: dict      = { 'abi': FlexUSDImplV0.abi, 'contractName': 'FlexUSDImplV0' }
    flex_impl        = ProjectContract(project, build=build, address=flex_usd.address)
  ### Initialize ###
  total_supply: int  = Wei('1000000 ether').to('wei')
  flex_impl.initialize(total_supply, {'from': admin})
  return flex_impl
