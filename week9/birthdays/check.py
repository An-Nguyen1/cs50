from cs50 import SQL
db = SQL("sqlite:///birthdays.db")
db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)","An",2,28)
