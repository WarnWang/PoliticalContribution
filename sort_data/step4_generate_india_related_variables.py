#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_generate_india_related_variables
# @Date: 2017-04-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constants as const

india_name_df = pd.read_excel(os.path.join(const.NAME_DATA_PATH, 'SouthAsianNames.xls'))
india_name_series = india_name_df['Name'].apply(lambda x: x.lower())


def generate_india_related_variables(df_path):
    df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, df_path))
    india_df1 = df[df[const.C_LNAME].isin(india_name_series)]
    india_df2 = df[df[const.C_FNAME].isin(india_name_series)]
    india_df = pd.concat([india_df1, india_df2], ignore_index=False).drop_duplicates()

    india_group = india_df.groupby(const.C_STATE)

    in_sta_df = pd.DataFrame()
    in_sta_df.loc[:, 'IN_contribution_amt'] = india_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_num'] = india_group[const.AMOUNT].count()

    # male df
    male_group = india_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_male_amt'] = male_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_male_num'] = male_group[const.AMOUNT].count()

    # female df
    female_group = india_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_female_amt'] = female_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_female_num'] = female_group[const.AMOUNT].count()

    # ppl related variables
    rep_ppl_group = india_group.apply(lambda x: x[x[const.R_PARTY] == 200]).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_amt_rep'] = rep_ppl_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_num_rep'] = rep_ppl_group[const.AMOUNT].count()

    # dem related variables
    dem_ppl_group = india_group.apply(lambda x: x[x[const.R_PARTY] == 100]).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_amt_dem'] = dem_ppl_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_num_dem'] = dem_ppl_group[const.AMOUNT].count()

    # male dem

    male_dem_group = dem_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_male_amt_dem'] = male_dem_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_male_num_dem'] = male_dem_group[const.AMOUNT].count()

    # female dem
    female_dem_group = dem_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_female_amt_dem'] = female_dem_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_female_num_dem'] = female_dem_group[const.AMOUNT].count()

    # male rep
    male_rep_group = rep_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'M']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_male_amt_rep'] = male_rep_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_male_num_rep'] = male_rep_group[const.AMOUNT].count()

    # female rep
    female_rep_group = rep_ppl_group.apply(lambda x: x[x[const.C_GENDER] == 'F']).groupby(const.C_STATE)
    in_sta_df.loc[:, 'IN_contribution_female_amt_rep'] = female_rep_group[const.AMOUNT].sum()
    in_sta_df.loc[:, 'IN_contribution_female_num_rep'] = female_rep_group[const.AMOUNT].count()

    return in_sta_df.reset_index(drop=False)


if __name__ == '__main__':
    import datetime

    file_list = os.listdir(const.INPUT_DATA_PATH)
    save_name = '20170414_IN_statistics'
    save_path = os.path.join(const.RESULT_PATH, '20170414_PPL_statistics')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    sta_dfs = []

    for data_file in file_list:
        print('{}: {}'.format(datetime.datetime.today(), data_file))
        firm_df = generate_india_related_variables(df_path=data_file)
        firm_df['year'] = int(data_file.split('.')[0].split('_')[-1])
        sta_dfs.append(firm_df)

    sta_df = pd.concat(sta_dfs, ignore_index=True)
    sta_df.to_pickle(os.path.join(save_path, '{}.p'.format(save_name)))
    sta_df.to_csv(os.path.join(save_path, '{}.csv'.format(save_name)))
