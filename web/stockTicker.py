import os 

import numpy as np
import pandas as pd

from datetime import datetime, date 
from sqlalchemy import create_engine
from geometricBrownianBridge import GeometricBrownianBridge


class StockTicker:
    """
    Interface for stock_price database
    """
    def __init__(self, conn_on_init = False):
        
        if conn_on_init:
            self._connect_to_database()

    # === 1. First Order Methods === # 

    def generate_prices(self, seed = None, **kwargs):
        """
        Generate random stock prices by samping Geo. Brownian Bridge 
        """
        self.gbb = GeometricBrownianBridge(**kwargs)
        self.gbb.generate_sample(seed = seed)

    def write_prices_to_database(self):
        """
        Write GBM sample to "stock_price' table 
        """
        df_ABC = pd.DataFrame({"TIME" : self.gbb.GBM_t.index, "ABC" : self.gbb.GBM_t.values})
        df_ABC.to_sql(name = "stock_price", con = self.engine, if_exists = "append", index = False)

    def get_latest_price_from_database(self):
        """
        Query database for last known stock price as of datetime.now()
        """
        sql = \
        """
        SELECT * FROM stock_price 
        WHERE "TIME" <= '{now}'
        ORDER BY "TIME" DESC
        LIMIT 1
        """.format(now = datetime.now().isoformat())

        payload = pd.read_sql(sql, self.engine).to_dict(orient = "records")[0]
        
        return payload 

    # === 2. Second Order Methods === # 

    def _connect_to_database(self):
        """
        Create database connection engine 
        """
        CONN_STRING = self._get_secret("postgres_conn_string")
        self.engine = create_engine(CONN_STRING)

    def _get_secret(self, secret):
        """
        Read secret under ./secret subdir
        """
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "secrets", secret)) as f_open:
            secret = f_open.read()

        return secret
