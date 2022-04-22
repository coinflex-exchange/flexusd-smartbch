#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/upgrades_v2.py
# VERSION: 	 1.0
# CREATED: 	 
# AUTHOR: 	 
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import List
from decimal import Decimal
### Project Contracts ###
from brownie import FlexUSD, FlexUSDImplV2, Contract, FlexUSDImplMock
### Third-Party Packages ###
from brownie.network.account import Account
from brownie.exceptions import VirtualMachineError
from pytest import fixture
### Local Modules ###
from . import *
from .v2 import deploy_impl, deploy_flexusd #Assume original contract deployed with v2 logic

BLUE: str  = '\033[1;34m'
RED: str   = '\033[1;31m'
NFMT: str  = '\033[0;0m'

@fixture
def flexusd_mock(admin: Account) -> FlexUSDImplMock:
  '''
  Deploy mock Implementation Logic Contract.
  '''
  print(f'{ BLUE }Event: flexUSD Implementation Logic V2 Deployment{ NFMT }')
  ### Deploy ###
  flex_usd: FlexUSDImplMock = FlexUSDImplMock.deploy({'from': admin})
  return flex_usd

def test_upgrade_to_zero(admin: Account, deploy_flexusd: FlexUSD):
  print('Test: Try upgrading to Zeoro Address')
  ### Prepare Parameters ###
  target: str = '0x0000000000000000000000000000000000000000'
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be zero address'

def test_upgrade_to_eoa(admin: Account, user_accounts: List[Account], deploy_flexusd: FlexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = user_accounts[0].address
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation is not a contract'

def test_upgrade_to_same_impl(admin: Account, deploy_flexusd: FlexUSD, deploy_impl: FlexUSDImplV2):
  print('Test: Try upgrading to same implementation address')
  ### Prepare Parameters ###
  target: str = deploy_impl.address
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be the same address'

def test_upgrade_from_non_owner(user_accounts: List[Account], deploy_flexusd: FlexUSD, flexusd_mock: FlexUSDImplMock):
  print('Test: Upgrading from a Non-Owner Account')
  ### Prepare Parameters ###
  target: str = flexusd_mock.address
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, {'from': user_accounts[0]})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert Ownable: caller is not the owner'


# Assume original contract is deployed with v2 logic
# Since the proxy contract itself was refactored, successful upgrade needs to be retested 
# Original deployment was with v2 logic, upgrade could be tested by ugrading v2 to v1/v0(not ideal path of upgrade, but suffices for the unit test)

def test_upgrade_successful_to_new_version(admin: Account, deploy_flexusd: FlexUSD, deploy_impl: FlexUSDImplV2, flexusd_mock: FlexUSDImplMock):
  print('Test: Upgrading Successfully')
  ### Prepare Parameters ###
  target: str = flexusd_mock.address
  totalSupply_amount_wei: Decimal
  ### Upgrade ###
  reverted: bool    = False
  flex_usd: FlexUSD = deploy_flexusd
  flexUSD_abi=Contract.from_abi('FlexUSD',flex_usd.address,deploy_impl.abi)
  totalSupply_before_upgrade=flexUSD_abi.totalSupply()
  try:
    flex_usd.upgrade(target, {'from': admin})
    flexUSD_upgraded_abi=Contract.from_abi('FlexUSD',flex_usd.address,flexusd_mock.abi)
    totalSupply_after_upgrade=flexUSD_upgraded_abi.totalSupply()
  except VirtualMachineError as err:
    reverted     = True
  assert reverted == False
  assert deploy_impl.totalSupply != flexUSD_upgraded_abi.totalSupply() # Storage is not shared, logic is;
  assert deploy_impl.owner()       == flexUSD_upgraded_abi.owner()       #deployed by the same key
  assert totalSupply_before_upgrade == totalSupply_after_upgrade