#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: setp3_generate_some_yearly_ppl_variables
# @Date: 2017-04-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const


def str2int(x):
    try:
        return int(x)

    except Exception:
        return x


def process_df(df_file):

    # load file and reformat party data type
    df_file_path = os.path.join(const.INPUT_DATA_PATH, df_file)
    df = pd.read_pickle(df_file_path)
    df.loc[:, const.R_PARTY] = df[const.R_PARTY].apply(str2int)
    df.to_pickle(df_file_path)

    # generate PPL level data
    ppl_df = df.dropna(subset=[const.C_LNAME, const.C_FNAME], how='all')
    ppl_group = ppl_df.groupby(const.C_STATE)

