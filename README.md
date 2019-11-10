# redis_cache :chart_with_upwards_trend:
Toy example of how to use Redis as a database query cache. 

## Usage
Deployment of the application is orchestrated by a `docker-compose.yml` file; to build and run all services, run `docker-compose up` at such file level. Once deployed, three services will be running: a `redis` instance, an instantiated (table defined, but no data) `postgres` database, and a `flask` web app.

The `flask` node serves as the control center of the entire application. Commands are invoked via the endpoints:

  1. `$host/populate` : Generates stock (ABC) price data from a Geometric Brownian Bridge and writes to `postgres`.
  2. `$host/start_cache` : Starts a process to query the latest stock price every 5 seconds and cache it to `redis`.
  3. `$host/get_cache` : Gets the stock price from `redis` cache.
