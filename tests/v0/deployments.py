#!/usr/bin/env python3.7
# coding:utf-8
# Copyright (C) 2019-2021 All rights reserved.
# FILENAME:  tests/v0/deployments.py
# VERSION: 	 1.0
# CREATED: 	 2021-08-20 14:45
# AUTHOR: 	 Aekasitt Guruvanich <sitt@coinflex.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Project Contracts ###
from brownie import flexUSDImplV0
### Local Modules ###
from tests import *
from . import deploy_impl as deploy_impl_v0 # used by wrap_flexusd_v0
### ANSI Coloring ###
BLUE: str  = '\033[1;34m'
NFMT: str  = '\033[0;0m'

def test_deployments(deploy_impl_v0: flexUSDImplV0, wrap_flexusd_v0: flexUSDImplV0):
  print(f'{ BLUE }Deployment Test #1: Deploy Implementation Logic and then flexUSD.{ NFMT }')
  impl_v0: flexUSDImplV0  = deploy_impl_v0
  flex_usd: flexUSDImplV0 = wrap_flexusd_v0
  ### Display Shared Logic and Separate Storage ###
  print(f'Implementation V0: { impl_v0 } (totalSupply={ impl_v0.totalSupply() }, admin={ impl_v0.owner() })')
  print(f'flexUSD: { flex_usd } (totalSupply={ flex_usd.totalSupply()}, admin={ flex_usd.owner() })')
  assert impl_v0.totalSupply() != flex_usd.totalSupply() # Storage is not shared, logic is;
  assert impl_v0.owner()       == flex_usd.owner()       # Initialized by the same key
