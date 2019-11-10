from datetime import datetime, time 

import numpy as np
import pandas as pd


class GeometricBrownianBridge:
    """
    Geometric Brownian Motion used to simulated stock price movements.
    """
    def __init__(self, start = None, end = None, freq = "S", mu = 0.3, sigma = 0.3, s_0 = 20, T = 1):
        
        self.start = pd.to_datetime(start) or datetime.combine(datetime.now().date(), time(9, 30))
        self.end   = pd.to_datetime(end)   or datetime.combine(datetime.now().date(), time(23, 0))
        self.freq  = freq
        self.mu    = mu
        self.sigma = sigma
        self.s_0   = s_0
        self.T     = 1


    def generate_sample(self, seed = None, output = False):
        """
        Random GBM sample w.r.t seed 
        """
        np.random.seed(seed)

        # define params 
        indx = pd.date_range(start = self.start, end = self.end, freq = self.freq)
        n    = len(indx)
        t    = np.linspace(0, self.T, n)
        dt   = float(self.T)/n

        # generate data 
        samp  = np.random.standard_normal(size = n)
        BM_t  = pd.Series(data = np.cumsum(samp)*np.sqrt(dt), index = indx)  
        X_t   = (self.mu - 0.5*self.sigma**2)*t + self.sigma*BM_t
        GBM_t = self.s_0*np.exp(X_t)

        self.GBM_t = GBM_t

        if output:
            return self.GBM_t

