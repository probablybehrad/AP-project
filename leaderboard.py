from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from database import Database


class LeaderboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.setWindowTitle("Leaderboard")
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
        layout.setContentsMargins(50,40,50,40)

        # ---------- Title ----------

        title = QLabel("🏆 LEADERBOARD")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("""
            background:#8E6AC8;
            color:#FFF3D6;
            border-radius:15px;
            padding:15px;
        """)

        layout.addWidget(title)
        layout.addSpacing(30)

        # ---------- Table ----------

        self.table = QTableWidget()

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Rank", "Username", "Score"]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setStyleSheet("""
        QTableWidget{
            background:white;
            color:black;
            border-radius:12px;
            gridline-color:#CFCFCF;
            font-size:15px;
        }

        QHeaderView::section{
            background:#8E6AC8;
            color:white;
            padding:8px;
            font-weight:bold;
            border:none;
        }
        """)

        layout.addWidget(self.table)

        layout.addSpacing(25)

        # ---------- Back Button ----------

        back_btn = QPushButton("Back")

        back_btn.setMinimumHeight(45)

        back_btn.setStyleSheet("""
            QPushButton{
                background:#F7D774;
                color:#212A3A;
                border-radius:12px;
                font-size:18px;
            }

            QPushButton:hover{
                background:#FFD54F;
            }
        """)

        back_btn.clicked.connect(self.close)

        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.load_scores()

    # ---------------------------------

    def load_scores(self):

        scores = self.db.get_top_scores()

        self.table.setRowCount(len(scores))

        for row, (username, score) in enumerate(scores):

            rank = QTableWidgetItem(str(row + 1))
            user = QTableWidgetItem(username)
            points = QTableWidgetItem(str(score))

            rank.setTextAlignment(Qt.AlignCenter)
            user.setTextAlignment(Qt.AlignCenter)
            points.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, rank)
            self.table.setItem(row, 1, user)
            self.table.setItem(row, 2, points)