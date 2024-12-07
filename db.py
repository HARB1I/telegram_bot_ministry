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

    def get_topic_title(self):
        with self.connection:
            return self.cursor.execute("SELECT title FROM topic").fetchall()

    def get_topic_id(self, title):
        with self.connection:
            result = self.cursor.execute("SELECT topic_id FROM topic WHERE title = ?", (title,)).fetchall()
            for row in result:
                id = str(row[0])
            return id

    def add_topic_title(self, title):
        with self.connection:
            return self.cursor.execute("INSERT INTO topic (title) VALUES (?)", (title,))

    def add_content(self, user_id, topic_id, content):
        with self.connection:
            return self.cursor.execute("INSERT INTO replies (user_id, topic_id, content) VALUES (?,?,?)", (user_id, topic_id, content))

    def delete_topic(self, topic_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM topic WHERE topic_id = ?", (topic_id,))

    def get_flag_add_topic(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT flag_add_topic FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def set_flag_add_topic(self, user_id, flag_add_topic):
        with self.connection:
            return self.cursor.execute("UPDATE users SET flag_add_topic = ? WHERE user_id = ?",(flag_add_topic, user_id,))

    def get_is_content(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT is_content FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def set_is_content(self, user_id, is_content):
        with self.connection:
            return self.cursor.execute("UPDATE users SET is_content = ? WHERE user_id = ?",(is_content, user_id,))

    def get_n_content(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT n_content FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                admin = str(row[0])
            return admin

    def set_n_content(self, user_id, n_content):
        with self.connection:
            return self.cursor.execute("UPDATE users SET n_content = ? WHERE user_id = ?",(n_content, user_id,))