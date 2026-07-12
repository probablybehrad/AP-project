from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from leaderboard import LeaderboardWindow
from database import Database


class GameOverWindow(QWidget):

    def __init__(self, username, score):
        super().__init__()

        self.username = username
        self.score = score

        self.db = Database()
        self.db.save_score(username, score)

        self.setWindowTitle("Game Over")
        self.resize(1000, 600)

        self.build_ui()

    def build_ui(self):

        self.setStyleSheet("""
        QWidget{
            background:#211A3A;
            color:white;
        }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # ---------- Title ----------

        title = QLabel("GAME OVER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 30, QFont.Bold))
        title.setStyleSheet("""
            background:#8E6AC8;
            color:#FFF3D6;
            border-radius:15px;
            padding:15px;
        """)

        layout.addWidget(title)

        # ---------- Username ----------

        player = QLabel(f"Player : {self.username}")
        player.setAlignment(Qt.AlignCenter)
        player.setFont(QFont("Arial", 18))

        layout.addWidget(player)

        # ---------- Score ----------

        score = QLabel(f"Score : {self.score}")
        score.setAlignment(Qt.AlignCenter)
        score.setFont(QFont("Arial", 22, QFont.Bold))
        score.setStyleSheet("color:#FFD54F;")

        layout.addWidget(score)

        layout.addSpacing(30)

        # ---------- Leaderboard ----------

        leaderboard_btn = QPushButton("Leaderboard")
        leaderboard_btn.setMinimumHeight(45)

        leaderboard_btn.setStyleSheet("""
        QPushButton{
            background:#8E6AC8;
            color:white;
            border-radius:12px;
            font-size:18px;
        }

        QPushButton:hover{
            background:#A57AE6;
        }
        """)

        leaderboard_btn.clicked.connect(self.open_leaderboard)

        layout.addWidget(leaderboard_btn)

        # ---------- Restart ----------

        restart_btn = QPushButton("Restart")
        restart_btn.setMinimumHeight(45)

        restart_btn.setStyleSheet("""
        QPushButton{
            background:#4CAF50;
            color:white;
            border-radius:12px;
            font-size:18px;
        }

        QPushButton:hover{
            background:#66BB6A;
        }
        """)

        restart_btn.clicked.connect(self.restart_game)

        layout.addWidget(restart_btn)

        # ---------- Exit ----------

        exit_btn = QPushButton("Exit")
        exit_btn.setMinimumHeight(45)

        exit_btn.setStyleSheet("""
        QPushButton{
            background:#E53935;
            color:white;
            border-radius:12px;
            font-size:18px;
        }

        QPushButton:hover{
            background:#EF5350;
        }
        """)

        exit_btn.clicked.connect(QApplication.quit)

        layout.addWidget(exit_btn)

        self.setLayout(layout)

    # ------------------------

    def open_leaderboard(self):

        self.lb = LeaderboardWindow()
        self.lb.show()

    # ------------------------

    def restart_game(self):

        self.close()

        # بعداً اینجا بازی دوباره اجرا می‌شود
        # from game import run_game
        # run_game(self.username)