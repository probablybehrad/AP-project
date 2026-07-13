import sqlite3
import hashlib


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        # ---------- Users ----------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        # ---------- Scores ----------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)

        # ---------- Games ----------
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1 TEXT NOT NULL,
            score1 INTEGER NOT NULL,
            player2 TEXT NOT NULL,
            score2 INTEGER NOT NULL
        )
        """)

        self.conn.commit()

    # ---------------- Password ----------------

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ---------------- Register ----------------

    def register(self, fullname, username, password):

        password = self.hash_password(password)

        try:
            self.cursor.execute("""
            INSERT INTO users(fullname,username,password)
            VALUES(?,?,?)
            """, (fullname, username, password))

            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    # ---------------- Login ----------------

    def login(self, username, password):

        password = self.hash_password(password)

        self.cursor.execute("""
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """, (username, password))

        return self.cursor.fetchone()

    # ---------------- User Exists ----------------

    def user_exists(self, username):

        self.cursor.execute("""
        SELECT id
        FROM users
        WHERE username=?
        """, (username,))

        return self.cursor.fetchone() is not None

    # ---------------- Get User ----------------

    def get_user(self, username):

        self.cursor.execute("""
        SELECT fullname, username
        FROM users
        WHERE username=?
        """, (username,))

        return self.cursor.fetchone()

    # ---------------- Change Password ----------------

    def change_password(self, username, new_password):

        new_password = self.hash_password(new_password)

        self.cursor.execute("""
        UPDATE users
        SET password=?
        WHERE username=?
        """, (new_password, username))

        self.conn.commit()

    # ---------------- Delete User ----------------

    def delete_user(self, username):

        self.cursor.execute("""
        DELETE FROM users
        WHERE username=?
        """, (username,))

        self.conn.commit()

    # ---------------- All Users ----------------

    def get_all_users(self):

        self.cursor.execute("""
        SELECT fullname, username
        FROM users
        ORDER BY fullname
        """)

        return self.cursor.fetchall()

    # ---------------- Save Score ----------------

    def save_score(self, username, score):

        self.cursor.execute("""
        INSERT INTO scores(username, score)
        VALUES(?, ?)
        """, (username, score))

        self.conn.commit()

    # ---------------- Save Game Result ----------------

    def save_game_result(self, player1, score1, player2, score2):

        self.cursor.execute("""
        INSERT INTO games(player1, score1, player2, score2)
        VALUES (?, ?, ?, ?)
        """, (player1, score1, player2, score2))

        self.conn.commit()

    # ---------------- Leaderboard ----------------

    def get_top_scores(self, limit=10):

        self.cursor.execute("""
        SELECT username, score
        FROM scores
        ORDER BY score DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    # ---------------- Best Score ----------------

    def get_best_score(self, username):

        self.cursor.execute("""
        SELECT MAX(score)
        FROM scores
        WHERE username=?
        """, (username,))

        result = self.cursor.fetchone()

        if result[0] is None:
            return 0

        return result[0]

    # ---------------- Close ----------------

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    db = Database()

    print("Database Ready")

    if db.register("Ali Ahmadi", "ali", "1234"):
        print("User Created")
    else:
        print("User Exists")

    user = db.login("ali", "1234")

    if user:
        print("Login Success")
    else:
        print("Wrong Username Or Password")

    db.close()