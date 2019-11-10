import time 
from stockTicker import StockTicker

from redis import Redis
from flask import Flask

app     = Flask(__name__)
redis   = Redis(host = 'redis', port = 6379)
sticker = StockTicker(conn_on_init = True)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/populate')
def populate_stock_price():
    sticker.generate_prices()
    sticker.write_prices_to_database()

    return "{} price ticks written to database!".format(sticker.gbb.GBM_t.shape[0])

@app.route('/start_cache')
def start_cache():
    while True:
        payload = sticker.get_latest_price_from_database()
        redis.set("TIME", payload.get("TIME").isoformat())
        redis.set("ABC",  payload.get("ABC"))
        time.sleep(5)

@app.route('/get_cache')
def get_cached_price():
    time  = redis.get("TIME").decode("utf-8") 
    price = redis.get("ABC").decode("utf-8") 

    return "Latest price of ABC is {} USD as of {}".format(round(float(price), 2), time) 


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True) # listen to public (w.r.t. container) IPs