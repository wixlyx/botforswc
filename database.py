import sqlite3


class Db:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def create_profile(self, tg_username, name, surname, city, role, year, description, superpower, photo, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `profile_list` (`tg_usename`,`name`, 'surname',"
                                       "`city`,'role','year',`description`, `superpower`, 'photo', 'tg_id') VALUES(?,?,?,?,?,?,?,?,?,?)",
                                       (tg_username, name, surname, city, role, year, description, superpower, photo, tg_id))

    def profile_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `profile_list` WHERE `tg_usename` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def delete(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `profile_list` WHERE `tg_usename` = ?", (user_id,))

    def get_info(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `profile_list` WHERE `tg_usename` = ?", (user_id,)).fetchall()

    def spam(self):
        with self.connection:
            return self.cursor.execute(f'''SELECT tg_id FROM profile_list''').fetchall()

    def insert_codewords(self, words):
        with self.connection:
            return self.cursor.execute("INSERT INTO `codewords` ('words') VALUES(?)", (words,))

    def is_admin(self, username):
        with self.connection:
            return self.cursor.execute("SELECT EXISTS (SELECT username FROM admin WHERE username = ?)", (username,)).fetchone()

    def get_info_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT 'description' FROM `profile_list` WHERE `tg_usename` = ?", (user_id,)).fetchone()

    def add_point(self, number, user_id):
        with self.connection:
            return self.cursor.execute(f"UPDATE profile_list SET points = points + ? WHERE tg_id = ?", (number, user_id))

    def leaders(self):
        with self.connection:
            return self.cursor.execute("SELECT tg_usename, points FROM profile_list GROUP BY tg_usename ORDER BY points ").fetchall()

    def null(self):
        with self.connection:
            return self.cursor.execute("UPDATE profile_list SET points = 0")

    def add_admin(self, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO admin (username) VALUES (?)", (username,))

    def delete_admin(self, username):
        with self.connection:
            return self.cursor.execute("DELETE FROM admin WHERE username = ?", (username,))






