import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname = ? WHERE user_id = ?",(nickname,user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?",(signup, user_id,))  

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                nick = str(row[0])
            return nick

    def get_is_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def set_is_admin(self, user_id, is_admin):
        with self.connection:
            return self.cursor.execute("UPDATE users SET is_admin = ? WHERE user_id = ?",(is_admin, user_id,))

    def get_signup_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup_admin FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def set_signup_admin(self, user_id, is_admin):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup_admin = ? WHERE user_id = ?",(is_admin, user_id,))