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
from brownie import flexUSD, flexUSDImplV0, Wei
from brownie.exceptions import ContractExists
from brownie.network.contract import ProjectContract
from brownie.project.main import get_loaded_projects, Project
### Local Modules ###
from . import *
from .accounts import *

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

def test_deployments(deploy_impl_v0: flexUSDImplV0, wrap_flexusd_v0: flexUSDImplV0):
  print(f'{ BLUE }Deployment Test #1: Deploy Implementation Logic and then flexUSD.{ NFMT }')
  impl_v0: flexUSDImplV0  = deploy_impl_v0
  flex_usd: flexUSDImplV0 = wrap_flexusd_v0
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V0: { impl_v0 } (totalSupply={ impl_v0.totalSupply() }, admin={ impl_v0.owner() })')
  print(f'flexUSD: { flex_usd } (totalSupply={ flex_usd.totalSupply()}, admin={ flex_usd.owner() })')
  assert impl_v0.totalSupply() != flex_usd.totalSupply() # Storage is not shared, logic is;
  assert impl_v0.owner()       == flex_usd.owner()       # Initialized by the same key
