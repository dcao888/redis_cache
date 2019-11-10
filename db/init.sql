CREATE DATABASE docker_db;
\connect docker_db;

CREATE TABLE stock_price (
  "TIME" TIMESTAMP,
  "ABC" FLOAT
);