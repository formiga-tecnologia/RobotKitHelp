import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from UI.UI_splash import SplashScreen
from UI.UI_Project_editor import ProjectSelector


app = QApplication(sys.argv)

splash = SplashScreen()
selector = ProjectSelector()


def show_selector():
    splash.close()
    selector.show()


QTimer.singleShot(3000, show_selector)

splash.show()

sys.exit(app.exec())