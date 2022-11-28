from aiogram import types, Bot
import sqlite3


class helldb:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

# User
    def user_exists(self, chat_id):
        result = self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,)).fetchall()
        return bool(len(result))

    def add_user(self, chat_id):
        result = self.cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
        self.conn.commit()
        return result

    def set_active(self, chat_id, active):
        return self.cursor.execute("UPDATE users SET active = ? WHERE chat_id = ?", (active, chat_id,))

    def get_user(self):
        return self.cursor.execute("SELECT chat_id, active FROM users").fetchall()

    def user_balance(self, chat_id):
        result = self.cursor.execute("SELECT balance FROM users WHERE chat_id = ?", (chat_id,)).fetchmany(1)
        return int(result[0][0])

    def set_balance(self, chat_id, balance):
        result = self.cursor.execute("UPDATE users SET balance = ? WHERE chat_id = ?", (balance, chat_id,))
        self.conn.commit()
        return result

# Item tg
    def get_inline_item_tg(self):
        return self.cursor.execute("SELECT productsid, name, price, amount FROM products_tg").fetchall()

    def get_item_tg(self, x):
        return self.cursor.execute("SELECT * FROM products_tg WHERE productsid = ?", (x,)).fetchone()

# Item vpn
    def get_inline_item_vpn(self):
        return self.cursor.execute("SELECT productsid, name, price, amount FROM products_vpn WHERE amount > 0").fetchall()

    def get_item_vpn(self, x):
        return self.cursor.execute("SELECT * FROM products_vpn WHERE productsid = ?", (x,)).fetchone()

    def set_item_vpn(self, productsid, amount):
        result = self.cursor.execute("UPDATE products_vpn SET amount = ? WHERE productsid = ?", (amount, productsid,))
        self.conn.commit()
        return result

# Qiwi
    def add_check(self, chat_id, balance, bill_id):
        self.cursor.execute("INSERT INTO 'check' (chat_id, balance, bill_id) VALUES (?,?,?)", (chat_id, balance, bill_id,))
        self.conn.commit()

    def get_check(self, bill_id):
        result = self.cursor.execute("SELECT * FROM 'check' WHERE bill_id = ?", (bill_id,)).fetchmany(1)
        if bool(len(result)):
            return result[0]

    def delete_check(self, bill_id):
        return self.cursor.execute("DELETE * FROM check WHERE bill_id  = ?", (bill_id,))

    def close(self):
        self.conn.close()