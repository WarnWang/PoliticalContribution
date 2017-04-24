#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_generate_some_yearly_ppl_variables
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
    df = df[df[const.AMOUNT] > 0]
    # df.loc[:, const.R_PARTY] = df[const.R_PARTY].apply(str2int)
    # df.loc[:, const.C_STATE] = df[const.C_STATE].dropna().apply(lambda x: x.upper())
    # df.to_pickle(df_file_path)

    # generate PPL level data
    ppl_df = df.dropna(subset=[const.C_LNAME, const.C_FNAME], how='all')
    ppl_group = ppl_df.groupby(const.C_STATE)

    ppl_sta_df = pd.DataFrame()
    ppl_sta_df.loc[:, 'PPL_contribution_amt'] = ppl_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_num'] = ppl_group[const.AMOUNT].count()

    # male df
    male_group = ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_male_amt'] = male_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_male_num'] = male_group[const.AMOUNT].count()

    # female df
    female_group = ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_female_amt'] = female_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_female_num'] = female_group[const.AMOUNT].count()

    # ppl related variables
    rep_ppl_group = ppl_group.apply(lambda x: x[x[const.R_PARTY] == 200]).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_amt_rep'] = rep_ppl_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_num_rep'] = rep_ppl_group[const.AMOUNT].count()

    # dem related variables
    dem_ppl_group = ppl_group.apply(lambda x: x[x[const.R_PARTY] == 100]).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_amt_dem'] = dem_ppl_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_num_dem'] = dem_ppl_group[const.AMOUNT].count()

    # male dem
    male_dem_group = dem_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_male_amt_dem'] = male_dem_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_male_num_dem'] = male_dem_group[const.AMOUNT].count()

    # female dem
    female_dem_group = dem_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_female_amt_dem'] = female_dem_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_female_num_dem'] = female_dem_group[const.AMOUNT].count()

    # male rep
    male_rep_group = rep_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_male_amt_rep'] = male_rep_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_male_num_rep'] = male_rep_group[const.AMOUNT].count()

    # female rep
    female_rep_group = rep_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    ppl_sta_df.loc[:, 'PPL_contribution_female_amt_rep'] = female_rep_group[const.AMOUNT].sum()
    ppl_sta_df.loc[:, 'PPL_contribution_female_num_rep'] = female_rep_group[const.AMOUNT].count()

    return ppl_sta_df.reset_index(drop=False)


if __name__ == '__main__':
    import datetime

    file_list = os.listdir(const.INPUT_DATA_PATH)
    save_path = os.path.join(const.RESULT_PATH, '20170414_PPL_statistics')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    sta_dfs = []

    for data_file in file_list:
        print('{}: {}'.format(datetime.datetime.today(), data_file))
        firm_df = process_df(df_file=data_file)
        firm_df['year'] = int(data_file.split('.')[0].split('_')[-1])
        sta_dfs.append(firm_df)

    sta_df = pd.concat(sta_dfs, ignore_index=True)
    sta_df.to_pickle(os.path.join(save_path, '20170414_PPL_statistics.p'))
    sta_df.to_csv(os.path.join(save_path, '20170414_PPL_statistics.csv'))
