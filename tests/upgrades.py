#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/upgrades.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-24 09:37
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import List
### Project Contracts ###
from brownie import flexUSD, flexUSDImplV0, flexUSDImplV1
### Third-Party Packages ###
from brownie.network.account import Account
from brownie.exceptions import VirtualMachineError
### Local Modules ###
from . import *
from .v0 import deploy_impl as deploy_impl, deploy_flexusd # Assume original contract deployed with v0 logic
from .v1 import deploy_impl as deploy_impl_v1

def test_upgrade_to_zero(admin: Account, deploy_flexusd: flexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = '0x0000000000000000000000000000000000000000'
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: flexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be zero address'

def test_upgrade_to_eoa(admin: Account, user_accounts: List[Account], deploy_flexusd: flexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = user_accounts[0].address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: flexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation is not a contract'

def test_upgrade_to_same_impl(admin: Account, deploy_flexusd: flexUSD, deploy_impl: flexUSDImplV0):
  print('Test: Try upgrading to same implementation address')
  ### Prepare Parameters ###
  target: str = deploy_impl.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: flexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert flexUSD: new implementation cannot be the same address'

def test_upgrade_from_non_owner(user_accounts: List[Account], deploy_flexusd: flexUSD, deploy_impl_v1: flexUSDImplV1):
  print('Test: Upgrading from a Non-Owner Account')
  ### Prepare Parameters ###
  target: str = deploy_impl_v1.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: flexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': user_accounts[0]})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert Ownable: caller is not the owner'

def test_upgrade_successful(admin: Account, deploy_flexusd: flexUSD, deploy_impl_v1: flexUSDImplV1):
  print('Test: Upgrading Successfully')
  ### Prepare Parameters ###
  target: str = deploy_impl_v1.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  flex_usd: flexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
  assert reverted == False
