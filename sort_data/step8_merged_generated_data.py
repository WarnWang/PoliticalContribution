#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step8_merged_generated_data
# @Date: 2017-04-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

root_path = const.RESULT_PATH

sta_result_path = ['20170413_firm_statistics', '20170414_PPL_statistics', '20170415_net_rep_statistics']

df = pd.DataFrame()

for path in sta_result_path:
    current_path = os.path.join(root_path, path)

    file_list = os.listdir(current_path)
    print(path)

    for f in file_list:
        if not f.endswith('.p'):
            continue

        print(f)

        if df.empty:
            df = pd.read_pickle(os.path.join(current_path, f))
        else:
            df.merge(pd.read_pickle(os.path.join(current_path, f)), on=[const.C_STATE, const.YEAR], how='outer')

    print()

df.to_pickle(os.path.join(const.RESULT_PATH, '20170420_generated_result.p'))
df.to_csv(os.path.join(const.RESULT_PATH, '20170420_generated_result.p'), index=False)
