#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: os_related_function
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os


def get_root_path():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return '/home/zigan/Documents/WangYouan/trading/ChineseStock'
        elif os.uname()[0] == 'Darwin':
            return '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock'
        else:
            return '/home/wangzg/Documents/WangYouan/research/PoliticalContribution'
    else:
        return r'C:\Users\CFID\Documents\ChinaStock'
