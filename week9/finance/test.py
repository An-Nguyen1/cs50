#from helpers import lookup
#print(lookup("AMZN"))
from cs50 import SQL
db = SQL("sqlite:///finance.db")
stock_symbol = "FACE"
transaction_type = "BUY"
name = "Astrazeneca plc - ADR"
per_price = 126.975
amount = 3
total = per_price*amount
user_id = 1
#db.execute("INSERT INTO transactions(stock_symbol, transaction_type, amount, total, user_id) VALUES (AMZN, BUY, 3, 91.2, 1)")
#order_number = db.execute("INSERT INTO transactions(stock_symbol, transaction_type, amount, total, user_id) VALUES (?, ?, ?, ?, ?)",stock_symbol,transaction_type,amount, total, user_id)
#db.execute("INSERT INTO stocks(stock_symbol, per_price, amount, total_price, user_id, order_number) VALUES (?,?, ?, ?, ?, ?)",stock_symbol, per_price, amount, total, user_id, order_number)

#db.execute("UPDATE stocks SET amount = ? JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ? AND stock_symbol = ?",amount, user_id,stock_symbol)
#stock = db.execute("SELECT * FROM stocks WHERE id = ?",id)
session = {"user_id":1}
"""session = {"user_id":1}
session["user_id"] = 2
stock_symbol = "A"
portfolio_id =  db.execute("SELECT id FROM portfolio WHERE user_id= ?", session["user_id"])[0]["id"]
#has_stocks = db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ? AND stock_symbol = ?", session["user_id"],stock_symbol)
stocks =  db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ?", session["user_id"])
db.execute("UPDATE stocks SET amount = amount + ?, per_price = ? WHERE  id = ?",2, 34, 3)
print(portfolio_id)"""
session["user_id"] = 1
stocks = db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ?", session["user_id"])
print(stocks)
