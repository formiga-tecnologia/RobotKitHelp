from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("RoboKitHelp")
        self.resize(500,250)

        layout = QVBoxLayout(self)

        title = QLabel("RoboKitHelp")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px;font-weight:bold;")

        subtitle = QLabel("Create your own Pixel Robot")
        subtitle.setAlignment(Qt.AlignCenter)

        loading = QLabel("Carregando...")
        loading.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(loading)