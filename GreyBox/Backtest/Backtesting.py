# -*- coding: utf-8 -*-
"""
@author: Kelian

"""


import numpy as np
import pandas as pd

from xbbg import blp


class TimeSeries(self, Liste):
    def __init__(self):
        return 1

    def GetRet(Liste, Start = "20150101"):
        Start = "20150101"
        End = pd.Timestamp.today().strftime("%Y%m%d")
    
        Res = blp.bdh(tickers= [x + " Equity" for x in Liste],start_date = Start , end_date = End)
        Res.columns = [x[0] for x in Res.columns]
        Ret = (np.log(Res) - np.log(Res.shift(1))).iloc[1:,:]
        Ret = Ret.T.mean()
        return Ret