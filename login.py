import json
from home import HomeWindow
import os

print(os.getcwd())

from PySide6.QtWidgets import (QWidget,QLabel,QLineEdit,QPushButton,QMessageBox,QVBoxLayout,QCheckBox,)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from database import Database
from register import RegisterWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = Database()

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.setWindowTitle(self.config["game_name"])
        self.resize(1000, 600)
        self.build_ui()

    def build_ui(self):

        # ---------- Background ----------
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1000, 600)
        self.background.setStyleSheet("background-color: #211A3A")

        self.background.lower()
        # ---------- Panel ----------
        self.panel = QWidget(self)
        self.panel.setGeometry(50,45,400,500)

        self.panel.setStyleSheet("""
            background:#8E6AC8;
            border-radius:20px;
        """)

        layout = QVBoxLayout()

        # ---------- Title ----------
        title = QLabel(self.config["game_name"])
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("jersey 10", 30, QFont.Bold))
        title.setStyleSheet("""
                            color:#FFF3D6;
                            border-radius:20px;
                            background:#211A3A;
                            padding:12px;
                            """)

        layout.addWidget(title)
        layout.addSpacing(20)

        # ---------- Username ----------
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setMinimumHeight(40)
        layout.addWidget(self.username)
        self.username.setStyleSheet("""
        QLineEdit{
            background-color: #D9D9D9;
            color: Black;
            border: 2px solid #21214D;
            border-radius: 10px;
            padding: 8px;
        }
        """)

        # ---------- Password ----------
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(40)
        layout.addWidget(self.password)
        self.password.setStyleSheet("""
        QLineEdit{
            background-color: #D9D9D9;
            color: Black;
            border: 2px solid #21214D;
            border-radius: 10px;
            padding: 8px;
        }
        """)

        layout.addSpacing(15)

        # ---------- Login Button ----------
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.login)

        login_btn.setStyleSheet("""
            QPushButton{
                background:#E07BE0;
                color:#212A3A;
                border-radius:10px;
                font-size:26px;
            }

            QPushButton:hover{
                background:#1976D2;
            }
        """)

        layout.addWidget(login_btn)

        # ---------- Register Button ----------
        register_btn = QPushButton("Register")
        register_btn.setMinimumHeight(45)
        register_btn.clicked.connect(self.register)

        register_btn.setStyleSheet("""
            QPushButton{
                background:#F7D774;
                color:#212A3A;
                border-radius:10px;
                font-size:26px;
            }

            QPushButton:hover{
                background:#2E7D32;
            }
        """)

        layout.addWidget(register_btn)

        layout.addStretch()

        self.panel.setLayout(layout)

    # ---------------- Login ----------------

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        if username == "" or password == "":
            QMessageBox.warning(
                self,
                "Error",
            "fill"
            )
            return

        user = self.db.login(username, password)

        if user:

            fullname = user[1]
            username = user[2]

            self.home = HomeWindow(fullname, username)
            self.home.show()

            self.close()

            # اینجا در پارت بعد Home باز می‌شود
        else:

            QMessageBox.warning(
                self,
                "Error",
                "نام کاربری یا رمز عبور اشتباه است."
            )

    # ---------------- Register ----------------

    def register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()