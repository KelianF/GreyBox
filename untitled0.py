# -*- coding: utf-8 -*-
"""
@author: Kelian

"""

import pandas as pd


import pandas_market_calendars as mcal

nyse = mcal.get_calendar('NYSE')

mcal.get_calendar_names()

"20200101"  in  nyse.holidays().holidays

str(nyse.holidays().holidays)[str(nyse.holidays().holidays[x])[:4] == "2020"]


Date = "20200101"

HolidayList = [str(x).replace("-","") for x in nyse.holidays().holidays if str(x)[:4] == Date[:4]]

if Date in HolidayList:
    str(pd.to_datetime(Date) + pd.DateOffset(days=1)).strftime("%Y%m%d")

pd.to_datetime(str(nyse.holidays().holidays[-5])).strftime("")
