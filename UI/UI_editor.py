from pathlib import Path

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtWidgets import (
    QDockWidget,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QListWidget,
    QMainWindow,
    QStatusBar,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
)
from PySide6.QtGui import QAction, QColor, QBrush, QPainter, QPen
from core.package import Package
from core.piece import RectElement
from core.render.preview_widget import PreviewWidget
from core.scene import PIECE_MIME_TYPE, WorldView
from PySide6.QtWidgets import QFileDialog

class PieceListWidget(QListWidget):

    def mimeData(self, items):

        mime_data = QMimeData()

        if items:
            piece_name = items[0].text()
            mime_data.setText(piece_name)
            mime_data.setData(PIECE_MIME_TYPE, piece_name.encode("utf-8"))

        return mime_data


class ExecutionWindow(QMainWindow):

    def __init__(self, placed_pieces, parent=None):

        super().__init__(parent)

        self.setWindowTitle("RoboKitHelp - Execucao")
        self.resize(900, 600)

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor("#d8d8d8"))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setFrameShape(QGraphicsView.NoFrame)

        self.setCentralWidget(self.view)

        self.render_pieces(placed_pieces)

    # -------------------------------------------------

    def render_pieces(self, placed_pieces):

        self.scene.clear()

        for placed in placed_pieces:

            piece = placed["piece"]
            base_x = placed["x"]
            base_y = placed["y"]

            for element in piece:

                if isinstance(element, RectElement):

                    rect = QGraphicsRectItem(
                        base_x + element.x,
                        base_y + element.y,
                        element.width,
                        element.height
                    )

                    rect.setBrush(QBrush(QColor(element.fill)))
                    rect.setPen(QPen(QColor(element.border), 1))

                    self.scene.addItem(rect)

        items_rect = self.scene.itemsBoundingRect()

        if items_rect.isValid() and not items_rect.isNull():
            margin = 80
            self.scene.setSceneRect(
                items_rect.adjusted(
                    -margin,
                    -margin,
                    margin,
                    margin
                )
            )
            self.view.fitInView(items_rect.adjusted(-40, -40, 40, 40), Qt.KeepAspectRatio)
        else:
            self.scene.setSceneRect(0, 0, 900, 600)


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

        run_menu = menu.addMenu("Executar")
        action_run = QAction("Executar", self)
        action_run.triggered.connect(self.run_project)
        run_menu.addAction(action_run)

        menu_windows = menu.addMenu("Janelas")

        Arquivo_menu =  menu.addMenu("Arquivo")

        action_new = QAction("Novo Script", self)
        action_new.triggered.connect(self.new_project)
        Arquivo_menu.addAction(action_new)

        action_open = QAction("Abrir Script", self)
        action_open.triggered.connect(self.open_project)
        Arquivo_menu.addAction(action_open)

        action_save = QAction("Salvar Script", self)
        action_save.triggered.connect(self.save_project)
        Arquivo_menu.addAction(action_save)

        action_exit = QAction("Sair", self)
        action_exit.triggered.connect(self.close)
        Arquivo_menu.addAction(action_exit)

        menu_windows.addAction(self.toolsDock.toggleViewAction())
        menu_windows.addAction(self.propertiesDock.toggleViewAction())
        menu_windows.addAction(self.scriptDock.toggleViewAction())

        menu.addMenu("Ajuda")

    # -------------------------------------------------

    def run_project(self):

        placed_pieces = self.world.placed_pieces()

        self.execution_window = ExecutionWindow(placed_pieces, self)
        self.execution_window.show()

        self.statusBar().showMessage("Projeto em execucao")

    # -------------------------------------------------

    def create_center(self):

        self.world = WorldView()
        self.world.set_package(self.package)

        self.setCentralWidget(self.world)

    # -------------------------------------------------

    def create_left_panel(self):

        self.toolsDock = QDockWidget("Pecas", self)

        self.pieces_list = PieceListWidget()
        self.pieces_list.setDragEnabled(True)
        self.pieces_list.setDefaultDropAction(Qt.CopyAction)
        self.pieces_list.setSelectionMode(QListWidget.SingleSelection)

        self.load_default_pieces()

        self.toolsDock.setWidget(self.pieces_list)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.toolsDock
        )

    # -------------------------------------------------

    def create_right_panel(self):

        self.propertiesDock = QDockWidget("Propriedades", self)

        self.properties_tree = QTreeWidget()

        self.properties_tree.setHeaderLabels(["Propriedade", "Valor"])

        self.prop_name = QTreeWidgetItem(self.properties_tree, ["Nome", "-"])
        self.prop_width = QTreeWidgetItem(self.properties_tree, ["Largura", "-"])
        self.prop_height = QTreeWidgetItem(self.properties_tree, ["Altura", "-"])
        self.prop_quantity = QTreeWidgetItem(self.properties_tree, ["Quantidade", "-"])

        self.propertiesDock.setWidget(self.properties_tree)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            self.propertiesDock
        )

    # -------------------------------------------------

    def create_bottom_panel(self):

        self.scriptDock = QDockWidget("Script", self)

        self.scriptEditor = QTextEdit()

        self.scriptEditor.setPlaceholderText(
            "# Escreva a logica do seu robo..."
        )

        self.scriptDock.setWidget(self.scriptEditor)

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            self.scriptDock
        )
    def new_project(self):

        self.scriptEditor.clear()

        self.statusBar().showMessage("Novo script criado")

    def open_project(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Script",
            "",
            "Python (*.py)"
        )

        if not filename:
            return

        try:

            with open(filename, "r", encoding="utf-8") as file:

                self.scriptEditor.setPlainText(file.read())

            self.statusBar().showMessage(f"Script carregado: {Path(filename).name}")

        except Exception as e:

            self.statusBar().showMessage(str(e))


    def save_project(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Script",
            "script.py",
            "Python (*.py)"
        )

        if not filename:
            return

        if not filename.endswith(".py"):
            filename += ".py"

        try:

            with open(filename, "w", encoding="utf-8") as file:

                file.write(self.scriptEditor.toPlainText())

            self.statusBar().showMessage(f"Script salvo: {Path(filename).name}")

        except Exception as e:
            self.statusBar().showMessage(str(e))
    # -------------------------------------------------

    def create_statusbar(self):

        status = QStatusBar()

        status.showMessage("Pronto")

        self.setStatusBar(status)

    # -------------------------------------------------
    # PREVIEW
    # -------------------------------------------------
    def on_piece_clicked(self, item):

        name = item.text()

        piece = self.package.get(name)

        if piece is None:
            self.previewWidget.set_piece(None)
            self.statusBar().showMessage("Peca nao encontrada")
            return

        self.previewWidget.set_piece(piece)
        self.update_piece_properties(piece)
        self.statusBar().showMessage(f"Peca selecionada: {piece.name}")

    def update_piece_properties(self, piece):

        self.prop_name.setText(1, piece.name)
        self.prop_width.setText(1, str(piece.width))
        self.prop_height.setText(1, str(piece.height))
        self.prop_quantity.setText(1, str(len(piece)))

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

            self.pieces_list.addItem("(Nenhuma peca encontrada)")

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
