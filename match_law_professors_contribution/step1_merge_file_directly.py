#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_merge_file_directly
# @Date: 22/4/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import dask.dataframe as dd
import pandas as pd

from constants import Constants as const

# Convert paper authors' name to uppercase
prof_name_set = pd.read_pickle(const.LAW_AUTHOR_FILE_PATH)
prof_name_set = pd.Series(list(prof_name_set)).apply(lambda x: x.upper())
prof_name_set.to_pickle(const.LAW_AUTHOR_FILE_PATH)

# Convert contributor name to uppercase
temp_data_path = os.path.join(const.TEMP_PATH, '20170423_PPL_data')
if not os.path.isdir(temp_data_path):
    os.makedirs(temp_data_path)

ori_files = os.listdir(const.INPUT_DATA_PATH)

if os.path.isfile(os.path.join(temp_data_path, 'data.hdf')):
    os.remove(os.path.join(temp_data_path, 'data.hdf'))

for f in ori_files:
    df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, f))
    df = df.dropna(subset=[const.C_LNAME, const.C_FNAME], how='all')
    df = df[df[const.IS_CORP] != 'corp']
    df[const.R_PARTY] = df[const.R_PARTY].apply(str)
    df[const.C_NAME] = df[const.C_NAME].apply(lambda x: x.upper())
    # df.to_pickle(os.path.join(temp_data_path, f))
    df.to_hdf(os.path.join(temp_data_path, 'data.hdf'), '/{}'.format(f.split('.')[0]),
              data_columns=True, dropna=False, format='table')

df = dd.read_hdf(os.path.join(temp_data_path, 'data.hdf'), key='/*')

contribute_df = df[df.contributor_name.isin(prof_name_set)]
contribute_df.to_hdf(os.path.join(temp_data_path, 'contribute.hdf'), key='/data_*',
                     mode='w')
