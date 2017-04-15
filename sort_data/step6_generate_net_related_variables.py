#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step6_generate_net_related_variables
# @Date: 2017-04-15
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

china_name_df = pd.read_excel(os.path.join(const.NAME_DATA_PATH, 'chinese_names.xls'))
china_name_series = china_name_df['name'].dropna().apply(lambda x: x.lower())
india_name_df = pd.read_excel(os.path.join(const.NAME_DATA_PATH, 'SouthAsianNames.xls'))
india_name_series = india_name_df['Name'].apply(lambda x: x.lower())


def generate_net_rep_data(df):
    rep_sum = df[df[const.R_PARTY] == 200][const.AMOUNT].sum()
    dem_sum = df[df[const.R_PARTY] == 100][const.AMOUNT].sum()
    return rep_sum - dem_sum


def generate_net_rep_data_from_dataframe(df):
    df_group = df.groupby(const.C_STATE)
    result_series = pd.Series()

    for key in df_group.groups.keys():
        sub_df = df_group.get_group(key)
        sub_group = sub_df.groupby(const.C_NAME)
        net_value = pd.Series()
        for name in sub_group.groups.keys():
            sub_sub_df = sub_group.get_group(name)
            net_value.loc[name] = generate_net_rep_data(sub_sub_df)
        result_series.loc[key] = net_value[net_value > 0].count()

    return result_series


def generate_net_data(data_file):
    df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, data_file))

    result_df = pd.DataFrame()

    firm_df = df[df[const.IS_CORP] == 'corp']
    result_df['Firm_contribution_net_rep_num'] = generate_net_rep_data_from_dataframe(firm_df)

    return result_df.reset_index(drop=False)
