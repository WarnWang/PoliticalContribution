#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_get_prof_contribution
# @Date: 23/4/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

ori_files = os.listdir(const.INPUT_DATA_PATH)
prof_name_series = pd.read_pickle(const.LAW_AUTHOR_FILE_PATH)
temp_data_path = os.path.join(const.TEMP_PATH, '20170423_PPL_data')
temp_result_path = os.path.join(temp_data_path, 'prof_contribution')

if not os.path.isdir(temp_result_path):
    os.makedirs(temp_result_path)

for f in ori_files:
    data_sheet_name = f.split('.')[0]
    df = pd.read_hdf(os.path.join(temp_data_path, 'data.hdf'), '/{}'.format(data_sheet_name))
    sub_df = df[df[const.C_NAME].isin(prof_name_series)]
    sub_df.to_pickle(os.path.join(temp_result_path, '{}.p'.format(data_sheet_name)))
    sub_df.to_csv(os.path.join(temp_result_path, '{}.csv'.format(data_sheet_name)), index=False)
