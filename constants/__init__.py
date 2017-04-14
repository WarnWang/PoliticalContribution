#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2017-04-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from constants.path_info import Path
from constants.parameters import Parameters


class Constants(Path, Parameters):
    DATE = 'date'
    CYCLE = 'cycle'
    AMOUNT = 'amount'
    C_NAME = 'contributor_name'
    C_LNAME = 'contributor_lname'
    C_FNAME = 'contributor_fname'
    C_MNAME = 'contributor_mname'
    C_TITLE = 'contributor_title'
    C_GENDER = 'contributor_gender'
    C_TYPE = 'contributor_type'
    C_STATE = 'contributor_state'
    C_CITY = 'contributor_city'
    IS_CORP = 'is_corp'
    R_PARTY = 'recipient_party'

    US_STATES = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
                 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
                 'AS', 'GU', 'MP', 'PR', 'VI', 'UM', 'FM', 'MH', 'PW'}
