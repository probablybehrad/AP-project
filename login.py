import json
import os
import session
from PySide6.QtGui import QPixmap

from home import HomeWindow

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from database import Database
from register import RegisterWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = Database()

        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.setWindowTitle("Fish Pop")
        self.resize(1000, 600)

        self.build_ui()

    def build_ui(self):

        # ---------- Background ----------

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1000, 600)
        pixmap = QPixmap("image/backgroundlogin.jpeg")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True) 
        self.background.lower()

        # ---------- Panel ----------
        self.panel = QWidget(self)
        self.panel.setGeometry(300, 120, 400, 350)
        self.panel.setStyleSheet("""
            background:rgba(247,88,162,140);
            border-radius:20px;
        """)

        layout = QVBoxLayout()

        # ---------- Title ----------
        title = QLabel("Fish Pop")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Jersey 10", 30, QFont.Bold))
        title.setStyleSheet("""
            color:#FFF3D6;
            background:#211A3A;
            border-radius:20px;
            padding:12px;
        """)

        layout.addWidget(title)
        layout.addSpacing(20)

        # ---------- Username ----------
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setMinimumHeight(40)
        self.username.setStyleSheet("""
            QLineEdit{
                background:#D9D9D9;
                color:black;
                border:2px solid #21214D;
                border-radius:10px;
                padding:8px;
            }
        """)
        layout.addWidget(self.username)

        # ---------- Password ----------
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(40)
        self.password.setStyleSheet("""
            QLineEdit{
                background:#D9D9D9;
                color:black;
                border:2px solid #21214D;
                border-radius:10px;
                padding:8px;
            }
        """)
        layout.addWidget(self.password)

        layout.addSpacing(15)

        # ---------- Login ----------
        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.login)

        login_btn.setStyleSheet("""
            QPushButton{
                background:rgb(0,51,0);
                color:#F7D774;
                border-radius:10px;
                font-size:26px;
            }

            QPushButton:hover{
                background:#1976D2;
            }
        """)

        layout.addWidget(login_btn)

        # ---------- Register ----------
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
                "Please enter username and password."
            )
            return

        user = self.db.login(username, password)

        if not user:
            QMessageBox.warning(
                self,
                "Error",
                "نام کاربری یا رمز عبور اشتباه است."
            )
            return

        fullname = user[1]
        username = user[2]

        # جلوگیری از ورود دوباره یک نفر
        for player in session.players:
            if player["username"] == username:
                QMessageBox.warning(
                    self,
                    "Error",
                    "This player has already logged in."
                )
                return

        # ذخیره بازیکن
        session.players.append({
            "fullname": fullname,
            "username": username
        })

        # فقط بازیکن اول وارد شده
        if len(session.players) == 1:

            QMessageBox.information(
                self,
                "Player 1",
                "Player 1 logged in successfully.\n\nNow Player 2, please login."
            )

            self.username.clear()
            self.password.clear()
            self.username.setFocus()

            return

        # هر دو بازیکن وارد شدند
        if len(session.players) == 2:

            self.home = HomeWindow(session.players)
            self.home.show()
            self.close()

    # ---------------- Register ----------------

    def register(self):

        self.register_window = RegisterWindow()
        self.register_window.show()