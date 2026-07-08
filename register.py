from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QVBoxLayout
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from database import Database


class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle("Register")
        self.resize(450, 500)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))

        layout.addWidget(title)
        layout.addSpacing(20)

        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Full Name")
        self.fullname.setMinimumHeight(40)
        layout.addWidget(self.fullname)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setMinimumHeight(40)
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(40)
        layout.addWidget(self.password)

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm Password")
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setMinimumHeight(40)
        layout.addWidget(self.confirm)

        layout.addSpacing(20)

        btn = QPushButton("Register")
        btn.setMinimumHeight(45)
        btn.clicked.connect(self.register)

        btn.setStyleSheet("""
            QPushButton{
                background:#4CAF50;
                color:white;
                border-radius:10px;
                font-size:15px;
            }

            QPushButton:hover{
                background:#2E7D32;
            }
        """)

        layout.addWidget(btn)

        self.setLayout(layout)

    def register(self):

        fullname = self.fullname.text().strip()
        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm.text()

        if not fullname or not username or not password or not confirm:
            QMessageBox.warning(
                self,
                "Error",
                "تمام فیلدها را پر کنید."
            )
            return

        if password != confirm:
            QMessageBox.warning(
                self,
                "Error",
                "رمزهای عبور یکسان نیستند."
            )
            return

        if self.db.user_exists(username):
            QMessageBox.warning(
                self,
                "Error",
                "این نام کاربری قبلاً ثبت شده است."
            )
            return

        ok = self.db.register(
            fullname,
            username,
            password
        )

        if ok:
            QMessageBox.information(
                self,
                "Success",
                "ثبت‌نام با موفقیت انجام شد."
            )
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Error",
                "خطا در ثبت اطلاعات."
            )