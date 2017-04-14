#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_reformat_data
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constants import Constants as const

original_data_path = '/home/wangzg/Documents/Data/DIME'

file_list = os.listdir(original_data_path)

useful_cols = [const.CYCLE, const.AMOUNT, const.C_NAME, const.C_FNAME, const.C_LNAME, const.C_GENDER, const.C_STATE,
               const.C_CITY, const.R_PARTY, const.IS_CORP]

# for f in file_list:
#     print('{}: {}'.format(datetime.datetime.today(), f))
#     if f.endswith('2012.csv') and f.startswith('contribDB'):
#         chunks = pd.read_csv(os.path.join(original_data_path, f), encoding="ISO-8859-1", chunksize=10 ** 6,
#                              iterator=True)
#
#     else:
#         continue
#
#     df_list = []
#
#     for chunk in chunks:
#         df_list.append(chunk[useful_cols])
#
#     df = pd.concat(df_list, ignore_index=True)
#
#     df.to_pickle(os.path.join(const.INPUT_DATA_PATH, '{}.p'.format(f.split('.')[0])))
#     chunks.close()

# input_file_list = os.listdir(const.INPUT_DATA_PATH)
input_file_list = ['contribDB_2010.p', 'contribDB_2002.p', 'contribDB_1990.p']

for f in input_file_list:
    print('{}: {}'.format(datetime.datetime.today(), f))
    df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, f))
    df = df[useful_cols]
    df.to_pickle(os.path.join(const.INPUT_DATA_PATH, f))
