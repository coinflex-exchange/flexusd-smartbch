#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v2/deployments.py
# VERSION: 	 1.0
# CREATED: 	 
# AUTHOR: 	
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import FlexUSDImplV2
### Local Modules ###
from tests import ( admin, user_accounts )
from . import ( deploy_impl, deploy_flexusd, wrap_flexusd )
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

def test_deployments(deploy_impl: FlexUSDImplV2, wrap_flexusd: FlexUSDImplV2):
  print(f'{ BLUE }Deployment Test #1: Deploy Implementation Logic and then flexUSD.{ NFMT }')
  impl_v2: FlexUSDImplV2  = deploy_impl
  flex_usd: FlexUSDImplV2 = wrap_flexusd
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V2: { impl_v2 } (totalSupply={ impl_v2.totalSupply() }, admin={ impl_v2.owner() })')
  print(f'flexUSD: { flex_usd } (totalSupply={ flex_usd.totalSupply()}, admin={ flex_usd.owner() })')
  assert impl_v2.totalSupply() != flex_usd.totalSupply() # Storage is not shared, logic is;
  assert impl_v2.owner()       == flex_usd.owner()       # Initialized by the same key
