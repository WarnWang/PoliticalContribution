#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step7_generate_net_related_variables_new_tech
# @Date: 2017-04-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd

from constants import Constants as const

china_name_df = pd.read_excel(os.path.join(const.NAME_DATA_PATH, 'chinese_names.xls'))
china_name_series = china_name_df['name'].dropna().apply(lambda x: x.lower())
india_name_df = pd.read_excel(os.path.join(const.NAME_DATA_PATH, 'SouthAsianNames.xls'))
india_name_series = india_name_df['Name'].apply(lambda x: x.lower())


def generate_net_rep_data_from_dataframe(df):
    df_group = df.groupby(const.C_STATE)
    rep_net_num_series = pd.Series()
    rep_net_amt_series = pd.Series()

    dem_net_num_series = pd.Series()
    dem_net_amt_series = pd.Series()

    for key in df_group.groups.keys():
        sub_df = df_group.get_group(key)
        sub_rep = sub_df[sub_df[const.R_PARTY] == 200]
        sub_dem = sub_df[sub_df[const.R_PARTY] == 100]
        sub_dem_sum = sub_dem.groupby(const.C_NAME)[const.AMOUNT].sum()
        sub_rep_sum = sub_rep.groupby(const.C_NAME)[const.AMOUNT].sum()
        net_sum = sub_rep_sum.subtract(sub_dem_sum, fill_value=0)
        rep_net_num_series.loc[key] = net_sum[net_sum > 0].size
        dem_net_num_series.loc[key] = net_sum[net_sum < 0].size
        rep_net_amt_series.loc[key] = net_sum.sum()
        dem_net_amt_series.loc[key] = -net_sum.sum()

    return rep_net_amt_series, rep_net_num_series, dem_net_amt_series, dem_net_num_series


def generate_net_data(data_file):
    df = pd.read_pickle(os.path.join(const.INPUT_DATA_PATH, data_file))
    df = df[df[const.AMOUNT] > 0]

    result_df = pd.DataFrame()

    firm_df = df[df[const.IS_CORP] == 'corp']
    result_series = generate_net_rep_data_from_dataframe(firm_df)
    prefix = 'Firm_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_amt', 'net_rep_num', 'net_dem_amt', 'net_dem_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    ppl_df = df.dropna(subset=[const.C_LNAME, const.C_FNAME], how='all')
    result_series = generate_net_rep_data_from_dataframe(ppl_df)
    prefix = 'PPL_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_amt', 'net_rep_num', 'net_dem_amt', 'net_dem_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    ppl_male_df = ppl_df[ppl_df[const.C_GENDER] == 'M']
    result_series = generate_net_rep_data_from_dataframe(ppl_male_df)
    prefix = 'PPL_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_male_amt', 'net_rep_male_num', 'net_dem_male_amt', 'net_dem_male_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    ppl_female_df = ppl_df[ppl_df[const.C_GENDER] == 'F']
    result_series = generate_net_rep_data_from_dataframe(ppl_female_df)
    prefix = 'PPL_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_female_amt', 'net_rep_female_num', 'net_dem_female_amt',
                                'net_dem_female_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    in_df = pd.concat([ppl_df[ppl_df[const.C_LNAME].isin(india_name_series)],
                       ppl_df[ppl_df[const.C_FNAME].isin(india_name_series)]], ignore_index=False
                      ).drop_duplicates()
    result_series = generate_net_rep_data_from_dataframe(in_df)
    prefix = 'IN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_amt', 'net_rep_num', 'net_dem_amt', 'net_dem_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    in_male_df = in_df[in_df[const.C_GENDER] == 'M']
    result_series = generate_net_rep_data_from_dataframe(in_male_df)
    prefix = 'IN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_male_amt', 'net_rep_male_num', 'net_dem_male_amt', 'net_dem_male_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    in_female_df = in_df[in_df[const.C_GENDER] == 'F']
    result_series = generate_net_rep_data_from_dataframe(in_female_df)
    prefix = 'IN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_female_amt', 'net_rep_female_num', 'net_dem_female_amt',
                                'net_dem_female_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    cn_df = pd.concat([ppl_df[ppl_df[const.C_LNAME].isin(china_name_series)],
                       ppl_df[ppl_df[const.C_FNAME].isin(china_name_series)]], ignore_index=False
                      ).drop_duplicates()
    result_series = generate_net_rep_data_from_dataframe(cn_df)
    prefix = 'CN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_amt', 'net_rep_num', 'net_dem_amt', 'net_dem_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    cn_male_df = cn_df[cn_df[const.C_GENDER] == 'M']
    result_series = generate_net_rep_data_from_dataframe(cn_male_df)
    prefix = 'CN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_male_amt', 'net_rep_male_num', 'net_dem_male_amt', 'net_dem_male_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]

    cn_female_df = cn_df[cn_df[const.C_GENDER] == 'F']
    result_series = generate_net_rep_data_from_dataframe(cn_female_df)
    prefix = 'CN_contribution'
    keys = []
    for i, suffix in enumerate(['net_rep_female_amt', 'net_rep_female_num', 'net_dem_female_amt',
                                'net_dem_female_num']):
        keys.append('{}_{}'.format(prefix, suffix))
        result_df['{}_{}'.format(prefix, suffix)] = result_series[i]
    return result_df.reset_index(drop=False)


if __name__ == '__main__':
    import datetime

    file_list = os.listdir(const.INPUT_DATA_PATH)
    save_name = '20170415_net_rep_statistics'
    save_path = os.path.join(const.RESULT_PATH, '20170415_net_rep_statistics')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    sta_dfs = []

    for data_file in file_list:
        print('{}: {}'.format(datetime.datetime.today(), data_file))
        tmp_df = generate_net_data(data_file=data_file)
        tmp_df['year'] = int(data_file.split('.')[0].split('_')[-1])
        sta_dfs.append(tmp_df)

    sta_df = pd.concat(sta_dfs, ignore_index=True)
    sta_df = sta_df.rename(index=str, columns={'index': const.C_STATE})
    sta_df.to_pickle(os.path.join(save_path, '{}.p'.format(save_name)))
    sta_df.to_csv(os.path.join(save_path, '{}.csv'.format(save_name)))
