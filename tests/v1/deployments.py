#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v1/deployments.py
# VERSION: 	 1.0
# CREATED: 	 2021-09-27 14:25
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import flexUSDImplV1
### Local Modules ###
from tests import ( admin, user_accounts )
from . import ( deploy_impl, deploy_flexusd, wrap_flexusd )
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

def test_deployments(deploy_impl: flexUSDImplV1, wrap_flexusd: flexUSDImplV1):
  print(f'{ BLUE }Deployment Test #1: Deploy Implementation Logic and then flexUSD.{ NFMT }')
  impl_v1: flexUSDImplV1  = deploy_impl
  flex_usd: flexUSDImplV1 = wrap_flexusd
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V1: { impl_v1 } (totalSupply={ impl_v1.totalSupply() }, admin={ impl_v1.owner() })')
  print(f'flexUSD: { flex_usd } (totalSupply={ flex_usd.totalSupply()}, admin={ flex_usd.owner() })')
  assert impl_v1.totalSupply() != flex_usd.totalSupply() # Storage is not shared, logic is;
  assert impl_v1.owner()       == flex_usd.owner()       # Initialized by the same key
