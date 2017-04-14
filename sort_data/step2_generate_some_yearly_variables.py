#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_generate_some_yearly_variables
# @Date: 2017-04-12
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


def generate_firm_variables(data_df):
    result_df = pd.DataFrame()
    corp_df = data_df[data_df[const.IS_CORP] == 'corp']
    groups = corp_df.groupby(const.C_STATE)
    result_df.loc[:, 'Firm_contribution_amt'] = groups[const.AMOUNT].sum()
    result_df.loc[:, 'Firm_contribution_num'] = groups[const.AMOUNT].count()

    corp_df = corp_df[corp_df[const.R_PARTY].notnull()]
    corp_df.loc[:, const.R_PARTY] = corp_df[const.R_PARTY].apply(str2int)
    dem_groups = corp_df[corp_df[const.R_PARTY] == 100].groupby(const.C_STATE)
    rep_groups = corp_df[corp_df[const.R_PARTY] == 200].groupby(const.C_STATE)
    result_df.loc[:, 'Firm_contribution_amt_rep'] = rep_groups[const.AMOUNT].sum()
    result_df.loc[:, 'Firm_contribution_amt_dem'] = dem_groups[const.AMOUNT].sum()
    result_df.loc[:, 'Firm_contribution_num_rep'] = rep_groups[const.AMOUNT].count()
    result_df.loc[:, 'Firm_contribution_num_dem'] = dem_groups[const.AMOUNT].count()
    return result_df.reset_index(drop=False)


if __name__ == '__main__':
    file_list = os.listdir(const.INPUT_DATA_PATH)

    sta_dfs = []

    for data_file in file_list:
        df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, data_file))
        firm_df = generate_firm_variables(df)
        firm_df['year'] = int(data_file.split('.')[0].split('_')[-1])
        sta_dfs.append(firm_df)

    sta_df = pd.concat(sta_dfs, ignore_index=True)
    sta_df.to_pickle(os.path.join(const.RESULT_PATH, '20170413_firm_statistics', '20170413_firm_statistics.p'))
    sta_df.to_csv(os.path.join(const.RESULT_PATH, '20170413_firm_statistics', '20170413_firm_statistics.csv'))
