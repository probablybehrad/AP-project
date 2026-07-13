from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


from leaderboard import LeaderboardWindow


class GameOverWindow(QWidget):

    def __init__(
        self,
        player1_name,
        player1_score,
        player1_bullet,
        player1_time,
        player2_name,
        player2_score,
        player2_bullet,
        player2_time
    ):
        super().__init__()

        self.player1_name = player1_name
        self.player1_score = player1_score
        self.player1_bullet = player1_bullet
        self.player1_time = player1_time

        self.player2_name = player2_name
        self.player2_score = player2_score
        self.player2_bullet = player2_bullet
        self.player2_time = player2_time

        self.setWindowTitle("Game Over")
        self.resize(1000, 600)

        self.build_ui()

    def build_ui(self):

        # ---------- Background ----------

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
        self.panel.setGeometry(300, 60, 400, 480)
        self.panel.setStyleSheet("""
            background:rgba(51,153,255,140);
            border-radius:20px;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        # ---------- Title ----------

        title = QLabel("GAME OVER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Jersey 10", 32, QFont.Bold))
        title.setStyleSheet("""
            color:rgb(150,0,0);
            background:#211A3A;
            border-radius:20px;
            padding:12px;
        """)

        layout.addWidget(title)
        layout.addSpacing(10)

        # ---------- Winner ----------

        if self.player1_score > self.player2_score:
            winner = self.player1_name
        elif self.player2_score > self.player1_score:
            winner = self.player2_name
        else:
            winner = "DRAW"

        winner_label = QLabel(f"🏆{winner}🏆")
        winner_label.setAlignment(Qt.AlignCenter)
        winner_label.setFont(QFont("Jersey 10", 22, QFont.Bold))
        winner_label.setStyleSheet("color:#FFD54F;")

        layout.addWidget(winner_label)
        layout.addSpacing(10)

        # ---------- Player 1 ----------

        p1 = QLabel(
    f"""
    Player 1 : {self.player1_name}
    Score : {self.player1_score}
        """)

        p1.setAlignment(Qt.AlignCenter)
        p1.setFont(QFont("Jersey 10", 16))
        layout.addWidget(p1)

        # ---------- Player 2 ----------

        p2 = QLabel(
    f"""
    Player 2 : {self.player2_name}
    Score : {self.player2_score}
         """)

        p2.setAlignment(Qt.AlignCenter)
        p2.setFont(QFont("Jersey 10", 16))

        layout.addWidget(p2)

        layout.addSpacing(20)

        # ---------- restart ----------

        restart_btn = QPushButton("Restart")
        restart_btn.setMinimumHeight(45)
        restart_btn.clicked.connect(self.restart_game)
        # ---------- Exit ----------

        exit_btn = QPushButton("Exit")
        exit_btn.setMinimumHeight(45)
        exit_btn.clicked.connect(QApplication.quit)

        for btn in [restart_btn, exit_btn]:
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

        self.panel.setLayout(layout)
    
    def restart_game(self):

        from extra_items import run_game

        self.close()

        result = run_game(
            self.player1_name,
            self.player2_name
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


