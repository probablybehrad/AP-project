import sys
from PySide6.QtWidgets import QApplication

from game_over import GameOverWindow


app = QApplication(sys.argv)

window = GameOverWindow("Ali", 3500)
window.show()

sys.exit(app.exec())