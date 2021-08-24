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
### Third-Party Packages ###
from brownie.network.account import Account
from brownie.exceptions import VirtualMachineError
### Local Modules ###
from . import *
from .accounts import *
from .deployments import *

def test_upgrade_to_zero(admin: Account, deploy_flexusd: FlexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = '0x0000000000000000000000000000000000000000'
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert FlexUSD: new implementation cannot be zero address'

def test_upgrade_to_eoa(admin: Account, user_accounts: List[Account], deploy_flexusd: FlexUSD):
  print('Test: Try upgrading to EOA')
  ### Prepare Parameters ###
  target: str = user_accounts[0].address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert FlexUSD: new implementation is not a contract'

def test_upgrade_to_same_impl(admin: Account, deploy_flexusd: FlexUSD, deploy_impl_v0: FlexUSDImplV0):
  print('Test: Try upgrading to same implementation address')
  ### Prepare Parameters ###
  target: str = deploy_impl_v0.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert FlexUSD: new implementation cannot be the same address'

def test_upgrade_from_non_owner(user_accounts: List[Account], deploy_flexusd: FlexUSD, deploy_impl_clone: FlexUSDImplV0):
  print('Test: Upgrading from a Non-Owner Account')
  ### Prepare Parameters ###
  target: str = deploy_impl_clone.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  reverted_msg: str = ''
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': user_accounts[0]})
  except VirtualMachineError as err:
    reverted     = True
    reverted_msg = err.message
  assert reverted == True
  assert reverted_msg == 'VM Exception while processing transaction: revert Ownable: caller is not the owner'

def test_upgrade_successful(admin: Account, deploy_flexusd: FlexUSD, deploy_impl_clone: FlexUSDImplV0):
  print('Test: Upgrading Successfully')
  ### Prepare Parameters ###
  target: str = deploy_impl_clone.address
  data: bytes = b''
  ### Upgrade ###
  reverted: bool    = False
  flex_usd: FlexUSD = deploy_flexusd
  try:
    flex_usd.upgrade(target, data, {'from': admin})
  except VirtualMachineError as err:
    reverted     = True
  assert reverted == False