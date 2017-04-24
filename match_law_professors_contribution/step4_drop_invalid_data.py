#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_drop_invalid_data
# @Date: 24/4/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

temp_data_path = os.path.join(const.TEMP_PATH, '20170423_PPL_data')
temp_result_path = os.path.join(temp_data_path, 'prof_contribution')

df = pd.read_pickle(os.path.join(temp_data_path, 'contribution.p'))
df = df[df[const.AMOUNT] > 0]
df.to_pickle(os.path.join(temp_data_path, 'contribution_dropna.p'))
df.to_csv(os.path.join(temp_data_path, 'contribution_dropna.csv'), index=False)
