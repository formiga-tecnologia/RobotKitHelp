from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QTextEdit,
    QListWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QStatusBar
)
from PySide6.QtCore import Qt
from pathlib import Path
from core.render.preview_widget import PreviewWidget
from core.package import Package
from core.scene import WorldView

class EditorWindow(QMainWindow):

    def __init__(self, project_path=None):
        super().__init__()

        self.package = Package()
        self.package.load(Path("assets") / "pieces")
        

        self.project_path = project_path

        project_name = "Sem Projeto"

        if project_path:
            project_name = Path(project_path).stem

        self.setWindowTitle(f"RoboKitHelp - {project_name}")

        self.setDockNestingEnabled(True)

        self.setDockOptions(
            QMainWindow.AllowNestedDocks |
            QMainWindow.AllowTabbedDocks |
            QMainWindow.AnimatedDocks
        )

        # Ordem correta
        self.create_center()
        self.create_left_panel()
        self.pieces_list.itemClicked.connect(self.on_piece_clicked)
        self.create_right_panel()
        self.create_bottom_panel()
        self.create_preview_panel()
        self.create_menu()
        self.create_statusbar()

        self.set_dark_theme()

    # -------------------------------------------------

    def create_menu(self):

        menu = self.menuBar()

        menu.addMenu("Arquivo")
        menu.addMenu("Editar")
        menu.addMenu("Exibir")
        menu.addMenu("Projeto")
        menu.addMenu("Executar")

        menu_windows = menu.addMenu("Janelas")

        menu_windows.addAction(self.toolsDock.toggleViewAction())
        menu_windows.addAction(self.propertiesDock.toggleViewAction())
        menu_windows.addAction(self.scriptDock.toggleViewAction())

        menu.addMenu("Ajuda")

    # -------------------------------------------------

    def create_center(self):

        self.world = WorldView()

        self.setCentralWidget(self.world)
    # -------------------------------------------------

    def create_left_panel(self):

        self.toolsDock = QDockWidget("Peças", self)

        self.pieces_list = QListWidget()

        self.load_default_pieces()

        self.toolsDock.setWidget(self.pieces_list)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.toolsDock
        )

    # -------------------------------------------------

    def create_right_panel(self):

        self.propertiesDock = QDockWidget("Propriedades", self)

        tree = QTreeWidget()

        tree.setHeaderLabels(["Propriedade", "Valor"])

        QTreeWidgetItem(tree, ["Nome", "Robot"])
        QTreeWidgetItem(tree, ["Posição", "(0,0)"])
        QTreeWidgetItem(tree, ["Rotação", "0"])
        QTreeWidgetItem(tree, ["Escala", "1"])

        self.propertiesDock.setWidget(tree)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            self.propertiesDock
        )

    # -------------------------------------------------

    def create_bottom_panel(self):

        self.scriptDock = QDockWidget("Script", self)

        editor = QTextEdit()

        editor.setPlaceholderText(
            "# Escreva a lógica do seu robô..."
        )

        self.scriptDock.setWidget(editor)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            self.scriptDock
        )

    # -------------------------------------------------

    def create_statusbar(self):

        status = QStatusBar()

        status.showMessage("Pronto")

        self.setStatusBar(status)

    # -------------------------------------------------
    # PREVIEW 
    # -------------------------------------------------
    def on_piece_clicked(self, item):
        from core.piece import Piece, RectElement

        piece = Piece(name=item.text())

        piece.add_rect(0, 0, 40, 40, "#888888")

        piece.add_rect(10, 10, 6, 6, "#000000")

        piece.add_rect(24, 10, 6, 6, "#000000")

        self.previewWidget.set_piece(piece)
        self.previewWidget.update()


    def create_preview_panel(self):

        self.previewDock = QDockWidget("Piece Preview", self)

        self.previewWidget = PreviewWidget()

        self.previewDock.setWidget(self.previewWidget)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            self.previewDock
        )

        # deixa tipo aba com script
        self.tabifyDockWidget(
            self.scriptDock,
            self.previewDock
        )

    # -------------------------------------------------
    def load_default_pieces(self):

        self.pieces_list.clear()

        pieces_folder = Path("assets") / "pieces"

        pieces_folder.mkdir(parents=True, exist_ok=True)

        for piece in sorted(pieces_folder.glob("*.rkp")):

            self.pieces_list.addItem(piece.stem)

        if self.pieces_list.count() == 0:

            self.pieces_list.addItem("(Nenhuma peça encontrada)")

    def set_dark_theme(self):

        self.setStyleSheet("""

        QMainWindow{
            background:#2b2b2b;
        }

        QMenuBar{
            background:#303030;
            color:white;
        }

        QMenuBar::item{
            background:transparent;
        }

        QMenuBar::item:selected{
            background:#505050;
        }

        QMenu{
            background:#353535;
            color:white;
        }

        QMenu::item:selected{
            background:#505050;
        }

        QDockWidget{
            color:white;
            font-weight:bold;
        }

        QListWidget,
        QTextEdit,
        QTreeWidget{

            background:#3a3d41;
            color:white;
            border:1px solid #555;
        }

        QLabel{
            color:white;
        }

        QStatusBar{
            background:#303030;
            color:white;
        }

        """)