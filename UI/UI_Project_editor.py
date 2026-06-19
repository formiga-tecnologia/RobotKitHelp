from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QInputDialog,
    QMessageBox
)

from core.project_manager import ProjectManager
from UI.UI_editor import EditorWindow


class ProjectSelector(QWidget):

    def __init__(self):
        super().__init__()

        self.editor = None

        self.setWindowTitle("RoboKitHelp")

        self.resize(520, 360)

        self.setStyleSheet("""

            QWidget{
                background:#2b2b2b;
                color:white;
                font-size:14px;
            }

            QLabel{
                font-size:22px;
                font-weight:bold;
            }

            QPushButton{

                background:#404040;
                border:1px solid #666;
                padding:12px;
                border-radius:6px;
            }

            QPushButton:hover{

                background:#565656;

            }

        """)

        layout = QVBoxLayout(self)

        title = QLabel("RoboKitHelp")

        subtitle = QLabel("Escolha uma opção")

        btn_new = QPushButton("Novo Projeto")

        btn_open = QPushButton("Abrir Projeto")

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        layout.addWidget(btn_new)
        layout.addWidget(btn_open)

        layout.addStretch()

        btn_new.clicked.connect(self.new_project)
        btn_open.clicked.connect(self.open_project)

    def new_project(self):

        name, ok = QInputDialog.getText(
            self,
            "Novo Projeto",
            "Nome do Projeto:"
        )

        if not ok or not name.strip():
            return

        directory = QFileDialog.getExistingDirectory(
            self,
            "Escolha onde salvar"
        )

        if not directory:
            return

        project = ProjectManager.create_project(directory, name)

        self.open_editor(project)

    def open_project(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Projeto",
            "",
            "RoboKitHelp (*.rhk)"
        )

        if not file_name:
            return

        self.open_editor(file_name)

    def open_editor(self, project_path):

        self.editor = EditorWindow(project_path)

        self.editor.showMaximized()

        self.close()