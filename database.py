import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        self.conn.commit()

    # هش کردن رمز
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ثبت نام
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

    # ورود
    def login(self, username, password):

        password = self.hash_password(password)

        self.cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        user = self.cursor.fetchone()

        return user

    # بررسی وجود کاربر
    def user_exists(self, username):

        self.cursor.execute("""
        SELECT id FROM users
        WHERE username=?
        """, (username,))

        return self.cursor.fetchone() is not None

    # دریافت اطلاعات کاربر
    def get_user(self, username):

        self.cursor.execute("""
        SELECT fullname,username
        FROM users
        WHERE username=?
        """, (username,))

        return self.cursor.fetchone()

    # تغییر رمز
    def change_password(self, username, new_password):

        new_password = self.hash_password(new_password)

        self.cursor.execute("""
        UPDATE users
        SET password=?
        WHERE username=?
        """, (new_password, username))

        self.conn.commit()

    # حذف کاربر
    def delete_user(self, username):

        self.cursor.execute("""
        DELETE FROM users
        WHERE username=?
        """, (username,))

        self.conn.commit()

    # لیست کاربران
    def get_all_users(self):

        self.cursor.execute("""
        SELECT fullname,username
        FROM users
        ORDER BY fullname
        """)

        return self.cursor.fetchall()

    # بستن دیتابیس
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