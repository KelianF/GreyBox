# -*- coding: utf-8 -*-
"""
@author: Kelian

"""



import pandas as pd
import numpy as np
import os

from xbbg import blp


#blp.bdh(tickers= Ticker,start_date = Start , end_date = End)


class Backtest:
        
    def __init__(self, Ticker):
        self.name = Ticker
        self.TimeSeries = self.Updatedb()
        self.returns = self.Returns()

        
        
        
    def Aggregate(self, Start = "20190101", End = pd.Timestamp.today().strftime("%Y%m%d")):
        Ticker = str(self.name)
        if isinstance(Ticker, list):
            dfAll = None
            for Tick in Ticker:
                Pointer = self.GetData(Tick, Start = "20190101", End = pd.Timestamp.today().strftime("%Y%m%d"))
                if dfAll is None:
                    dfAll = Pointer
                else:
                    dfAll = pd.concat((dfAll, Pointer), axis = 1)
        else: 
            dfAll = self.GetData(Ticker, Start = "20190101", End = pd.Timestamp.today().strftime("%Y%m%d"))
        return dfAll
    
    
    def BloombergRequest(Ticker, Start, End):
        Pointer = blp.bdh(tickers= [Ticker],start_date = Start , end_date = End)
        Pointer.index = Pointer.index.strftime("%Y%m%d").astype(int)
        Pointer.columns = [Ticker]
        return Pointer
    
    
    def GetData(self, Start = "20190101", End = pd.Timestamp.today().strftime("%Y%m%d")):
        Ticker = str(self.name)
        if Ticker + ".csv" in os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET"):   # Folder Location
            #print("Got From DataBase")
            Pointer = pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index_col=0)
            if Start < str(Pointer.index.min()):
                Point = self.BloombergRequest(Ticker, Start, str(Pointer.index.min()))
                Pointer = pd.concat((Pointer, Point), axis = 0)
            if End > str(Pointer.index.max()):
                Point = self.BloombergRequest(Ticker, str(Pointer.index.max()), End)
                Pointer = pd.concat((Pointer, Point), axis = 0)
            Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index=True)
            return Pointer
        else:
            Pointer = self.BloombergRequest(Ticker, Start, End)
            Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index=True)
            return Pointer
    
    

        
    def Updatedb(self, Start = "20190101", End = pd.Timestamp.today().strftime("%Y%m%d")):
        
        Ticker = str(self.name)
        print(len(Ticker), type(Ticker), Ticker)
        if Ticker + ".csv" in os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET"):   # Folder Location
            #print("Got From DataBase")
            Pointer = pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index_col=0)
            if str(Pointer.index.max()) < End:
                Pointer2 = blp.bdh(tickers= [Ticker],start_date = str(Pointer.index.max()) , end_date = End)
                if len(Pointer2[Pointer2.index > str(Pointer.index.max())]) != 0:
                    Pointer2 = Pointer2.iloc[1:,:]
                    Pointer2.index = Pointer2.index.strftime("%Y%m%d")
                    Pointer2.columns = [Ticker]
                    Pointer = pd.concat((Pointer, Pointer2), axis = 0)
                Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index=True)
                    
            return Pointer
        else:
            Pointer = blp.bdh(tickers= [Ticker],start_date = "20190101" , end_date = "20200101")
            Pointer.index = Pointer.index.strftime("%Y%m%d")
            Pointer.columns = [Ticker]
            Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\MARKET\\" + Ticker + ".csv", index=True)
            return Pointer
    
    def Returns(self, method = "Logarithmic"):
        if method[:3] == "Log":
            return (np.log(self.TimeSeries) - np.log(self.TimeSeries.shift(1))).iloc[1:,:]
        elif method[:3] == "Ari":
            return ((self.TimeSeries/self.TimeSeries.shift(1))-1).iloc[1:,:]


class Metrics:
    def __init__(self, name):
        self.name = name
        self.returns = self.GetRet()
        
        self.Benchmark = self.Benchmark()
        self.Beta = self.BetaCalc()
        
        self.Sharpe = self.Sharpe()
        self.Treynor = self.TreynorRatio()
        
    def GetRet(self):
        return Backtest(self.name).Returns()
    
    def Benchmark(self, Name = "SPX Index"):
        return Backtest(Name).Returns()
        
    def Average_Returns(self):
        return self.returns.mean()
    
    def Average_vol(self):
        return self.returns.std()
    
    def BetaCalc(self):
        return pd.concat((self.returns, self.Benchmark), axis=1).dropna().corr().iloc[1,0]
        
    def Sharpe(self):
        return np.sqrt(252) * self.returns.mean() / self.returns.std()
    
    def TreynorRatio(self):
        return np.sqrt(252) * self.Average_Returns() / self.Beta
    
 
 
 
 
 
 
 
 
 
 
 
 

    
    
    
    
    
    