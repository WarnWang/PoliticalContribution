#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from utilities.os_related_function import get_root_path


class Path(object):
    ROOT_PATH = get_root_path()

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')

    NAME_DATA_PATH = os.path.join(DATA_PATH, 'names')
    INPUT_DATA_PATH = os.path.join(DATA_PATH, 'formatted_input_data')
    ORI_DATA_PATH = os.path.join(DATA_PATH, 'input_data')
    LAW_AUTHOR_FILE_PATH = os.path.join(DATA_PATH, 'law_author_list', '20170422_author_upper_name_series.p')
