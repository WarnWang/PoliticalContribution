#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_reformat_data
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

original_data_path = '/home/wangzg/Documents/Data/DIME'

file_list = os.listdir(original_data_path)

for f in file_list:
    if f.endswith('csv') and f.startswith('contribDB'):
        df = pd.read_csv(os.path.join(original_data_path, f))

    else:
        continue

    df[const.DATE] = pd.to_datetime(df[const.DATE])

    df.to_pickle(os.path.join(const.INPUT_DATA_PATH, '{}.p'.format(f.split('.')[0])))
