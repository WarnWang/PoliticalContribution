#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_merge_data
# @Date: 23/4/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

temp_data_path = os.path.join(const.TEMP_PATH, '20170423_PPL_data')
temp_result_path = os.path.join(temp_data_path, 'prof_contribution')

df_list = []
file_list = os.listdir(temp_result_path)

for f in file_list:
    if not f.endswith('.p'):
        continue

    df_list.append(pd.read_pickle(os.path.join(temp_result_path, f)))

df = pd.concat(df_list, ignore_index=True)

df.to_pickle(os.path.join(temp_data_path, 'contribution.p'))
df.to_csv(os.path.join(temp_data_path, 'contribution.csv'), index=False)
