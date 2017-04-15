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

    ppl_df = df.dropna(subset=[const.C_LNAME, const.C_FNAME], how='all')
    result_df['PPL_contribution_net_rep_num'] = generate_net_rep_data_from_dataframe(ppl_df)

    ppl_male_df = ppl_df[ppl_df[const.C_GENDER] == 'M']
    result_df['PPL_contribution_net_rep_male_num'] = generate_net_rep_data_from_dataframe(ppl_male_df)

    ppl_female_df = ppl_df[ppl_df[const.C_GENDER] == 'F']
    result_df['PPL_contribution_net_rep_female_num'] = generate_net_rep_data_from_dataframe(ppl_female_df)

    in_df = pd.concat([ppl_df[ppl_df[const.C_LNAME].isin(india_name_series)],
                       ppl_df[ppl_df[const.C_FNAME].isin(india_name_series)]], ignore_index=False
                      ).drop_duplicates()
    result_df['IN_contribution_net_rep_num'] = generate_net_rep_data_from_dataframe(in_df)

    in_male_df = in_df[in_df[const.C_GENDER] == 'M']
    result_df['IN_contribution_net_rep_male_num'] = generate_net_rep_data_from_dataframe(in_male_df)

    in_female_df = in_df[in_df[const.C_GENDER] == 'F']
    result_df['IN_contribution_net_rep_female_num'] = generate_net_rep_data_from_dataframe(in_female_df)

    cn_df = pd.concat([ppl_df[ppl_df[const.C_LNAME].isin(china_name_series)],
                       ppl_df[ppl_df[const.C_FNAME].isin(china_name_series)]], ignore_index=False
                      ).drop_duplicates()
    result_df['CH_contribution_net_rep_num'] = generate_net_rep_data_from_dataframe(cn_df)

    cn_male_df = cn_df[cn_df[const.C_GENDER] == 'M']
    result_df['CH_contribution_net_rep_male_num'] = generate_net_rep_data_from_dataframe(cn_male_df)

    cn_female_df = cn_df[cn_df[const.C_GENDER] == 'F']
    result_df['CH_contribution_net_rep_female_num'] = generate_net_rep_data_from_dataframe(cn_female_df)

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
    sta_df.to_pickle(os.path.join(save_path, '{}.p'.format(save_name)))
    sta_df.to_csv(os.path.join(save_path, '{}.csv'.format(save_name)))
