CREATE TABLE transactions(
  order_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  transaction_type TEXT NOT NULL,
  stock_symbol TEXT NOT NULL,
  amount int NOT NULL,
  total NUMERIC NOT NULL,
  portfolio_id int,
  FOREIGN KEY (portfolio_id) REFERENCES portfolio(id)
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  hash TEXT NOT NULL,
  cash NUMERIC NOT NULL DEFAULT 10000.00,
  portfolio_id int,
  FOREIGN KEY (portfolio_id) REFERENCES portfolio(id)
);

DROP TABLE transactions;
DROP TABLE users;
DROP TABLE portfolio;
DROP TABLE stocks;

CREATE TABLE portfolio(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  user_id int NOT NULL NOT NULL UNIQUE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE stocks(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  stock_symbol TEXT,
  name TEXT,
  per_price NUMERIC NOT NULL,
  amount int NOT NULL,
  portfolio_id int,
  FOREIGN KEY (portfolio_id) REFERENCES portfolio(id)
);
SELECT stock_id FROM stocks JOIN portfolio ON portfolio.stock_id = stocks.id;
SELECT * FROM transactions WHERE person_id = 1;
INSERT INTO portfolio (user_id) VALUES (1)
INSERT INTO transactions(stock_symbol, transaction_type, amount, total, user_id) VALUES ("AMZN", "BUY", 3, 91.2, 1);
INSERT INTO stocks(stock_symbol, per_price, amount, total_price, user_id, order_number) VALUES ("AMZN",30.4, 3, 91.2, 6,7);
