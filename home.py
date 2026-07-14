from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from game_over import GameOverWindow

class HomeWindow(QWidget):

    def __init__(self, players):
        super().__init__()

        self.players = players

        self.player1 = players[0]
        self.player2 = players[1]

        self.setWindowTitle("Home")
        self.resize(1000, 600)

        self.build_ui()

    def start_game(self):

        self.hide()

        from extra_items import run_game

        result = run_game(
            self.player1["username"],
            self.player2["username"]
        )

        self.game_over = GameOverWindow(
            result["player1_name"],
            result["player1_score"],
            result["player1_bullet"],
            result["player1_time"],

            result["player2_name"],
            result["player2_score"],
            result["player2_bullet"],
            result["player2_time"]
        )

        self.game_over.show()

        self.close()

    def build_ui(self):
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1000, 600)

        pixmap = QPixmap("image/mainbackground.jpg")
        self.background.setPixmap(
            pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )

        self.background.lower()
        # ---------- Panel ----------
        self.panel = QWidget(self)
        self.panel.setGeometry(300, 120, 400, 380)
        self.panel.setStyleSheet("""
            background:rgba(247,88,162,140);
            border-radius:20px;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome")
        title.setFont(QFont("Jersey 10", 54, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        p1 = QLabel(
            f"Player 1 : {self.player1['fullname']} ({self.player1['username']})"
        )
        p1.setAlignment(Qt.AlignCenter)
        p1.setFont(QFont("Jersey 10", 16))

        p2 = QLabel(
            f"Player 2 : {self.player2['fullname']} ({self.player2['username']})"
        )
        p2.setAlignment(Qt.AlignCenter)
        p2.setFont(QFont("Jersey 10", 16))

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(p1)
        layout.addWidget(p2)
        layout.addSpacing(40)

        # ---------- Start Game ----------

        start_btn = QPushButton("Start Game")
        start_btn.setMinimumHeight(45)
        start_btn.clicked.connect(self.start_game)

        # ---------- Profile ----------

        profile_btn = QPushButton("Profile")
        profile_btn.setMinimumHeight(45)
        profile_btn.clicked.connect(self.profile)

        # ---------- Logout ----------

        logout_btn = QPushButton("Logout")
        logout_btn.setMinimumHeight(45)
        logout_btn.clicked.connect(self.logout)

        buttons = [
            start_btn,
            profile_btn,
            logout_btn
        ]

        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton{
                    background:#000066;
                    color:white;
                    border-radius:10px;
                    font-size:15px;
                    padding:10px;
                }

                QPushButton:hover{
                    background:#1976D2;
                }
            """)

            layout.addWidget(btn)

        self.setLayout(layout)

    # -----------------------------

    def profile(self):

        QMessageBox.information(
            self,
            "Players",
            f"""
Player 1:
{self.player1['fullname']}
{self.player1['username']}

-------------------------

Player 2:
{self.player2['fullname']}
{self.player2['username']}
"""
        )

    # -----------------------------

    def settings(self):

        QMessageBox.information(
            self,
            "Settings",
            "NOT READY"
        )

    # -----------------------------

    def logout(self):

        self.close()