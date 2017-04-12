#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_generate_some_yearly_variables
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const


def generate_firm_variables(data_df):
    corp_df = data_df[data_df[const.IS_CORP] == 'corp']