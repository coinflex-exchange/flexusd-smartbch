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
### Project Contracts ###
from brownie import FlexUSD, flexUSDImplV0, flexUSDImplV1,FlexUSDImplV2
### Third-Party Packages ###
from brownie.network.account import Account
from brownie.exceptions import VirtualMachineError
### Local Modules ###
from . import *
from .v0 import deploy_impl as deploy_impl_v0
from .v1 import deploy_impl as deploy_impl_v1
from .v2 import deploy_impl as deploy_impl, deploy_flexusd as deploy_flexusd_v2 #Assume original contract deployed with v2 logic

def test_upgrade_to_zero(admin: Account, deploy_flexusd_v2: FlexUSD):
  print('Test: Try upgrading to Zeoro Address')
  ### Prepare Parameters ###
  target: str = '0x0000000000000000000000000000000000000000'
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be zero address'

def test_upgrade_to_eoa(admin: Account, user_accounts: List[Account], deploy_flexusd_v2: FlexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = user_accounts[0].address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation is not a contract'

def test_upgrade_to_same_impl(admin: Account, deploy_flexusd_v2: FlexUSD, deploy_impl: FlexUSDImplV2):
  print('Test: Try upgrading to same implementation address')
  ### Prepare Parameters ###
  target: str = deploy_impl.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be the same address'

def test_upgrade_from_non_owner(user_accounts: List[Account], deploy_flexusd_v2: FlexUSD, deploy_impl: FlexUSDImplV2):
  print('Test: Upgrading from a Non-Owner Account')
  ### Prepare Parameters ###
  target: str = deploy_impl.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': user_accounts[0]})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert Ownable: caller is not the owner'


# Assume original contract is deployed with v2 logic
# Since the proxy contract itself was refactored, successful upgrade needs to be retested 
# Original deployment was with v2 logic, upgrade could be tested by ugrading v2 to v1/v0(not ideal path of upgrade, but suffices for the unit test)

def test_upgrade_successful_to_v1(admin: Account, deploy_flexusd_v2: FlexUSD, deploy_impl_v1: flexUSDImplV1):
  print('Test: Upgrading Successfully')
  ### Prepare Parameters ###
  target: str = deploy_impl_v1.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
  assert reverted == False

def test_upgrade_successful_to_v0(admin: Account, deploy_flexusd_v2: FlexUSD, deploy_impl_v0: flexUSDImplV0):
  print('Test: Upgrading Successfully')
  ### Prepare Parameters ###
  target: str = deploy_impl_v0.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  flex_usd: FlexUSD = deploy_flexusd_v2
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
  assert reverted == False