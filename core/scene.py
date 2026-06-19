from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView
)

from core.piece import RectElement


PIECE_MIME_TYPE = "application/x-robokit-piece"


class PieceGraphicsItem(QGraphicsItemGroup):

    LABEL_HEIGHT = 20
    LABEL_GAP = 6
    LABEL_PADDING = 8

    def __init__(self, piece):

        super().__init__()

        self.piece = piece

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self._build_label()
        self._build_piece()

    # --------------------------------------------------------

    def _build_label(self):

        text = QGraphicsSimpleTextItem(self.piece.name)

        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        text.setFont(font)
        text.setBrush(QBrush(QColor("#d8d8d8")))

        text_rect = text.boundingRect()
        label_width = max(
            self.piece.width,
            text_rect.width() + self.LABEL_PADDING * 2
        )

        label = QGraphicsRectItem(
            0,
            -(self.LABEL_HEIGHT + self.LABEL_GAP),
            label_width,
            self.LABEL_HEIGHT
        )
        label.setBrush(QBrush(QColor(45, 48, 52, 220)))
        label.setPen(QPen(QColor("#6a6a6a"), 1))

        text.setPos(
            (label_width - text_rect.width()) / 2,
            -(self.LABEL_HEIGHT + self.LABEL_GAP) +
            (self.LABEL_HEIGHT - text_rect.height()) / 2 - 1
        )

        self.addToGroup(label)
        self.addToGroup(text)

    # --------------------------------------------------------

    def _build_piece(self):

        for element in self.piece:

            if isinstance(element, RectElement):

                rect = QGraphicsRectItem(
                    element.x,
                    element.y,
                    element.width,
                    element.height
                )

                rect.setBrush(QBrush(QColor(element.fill)))
                rect.setPen(QPen(QColor(element.border), 1))

                self.addToGroup(rect)


class WorldScene(QGraphicsScene):

    GRID_SIZE = 32

    def __init__(self):

        super().__init__()

        # Área inicial do mundo
        self.setSceneRect(-5000, -5000, 10000, 10000)

        self.setBackgroundBrush(QColor("#2b2b2b"))

    # --------------------------------------------------------

    def drawBackground(self, painter: QPainter, rect: QRectF):

        super().drawBackground(painter, rect)

        grid_pen = QPen(QColor(65, 65, 65))
        grid_pen.setWidth(1)

        painter.setPen(grid_pen)

        left = int(rect.left()) - (int(rect.left()) % self.GRID_SIZE)
        top = int(rect.top()) - (int(rect.top()) % self.GRID_SIZE)

        x = left

        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self.GRID_SIZE

        y = top

        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self.GRID_SIZE


# =====================================================================


class WorldView(QGraphicsView):

    def __init__(self):

        super().__init__()

        self.scene = WorldScene()

        self.setScene(self.scene)

        self.setRenderHint(QPainter.Antialiasing)

        self.setViewportUpdateMode(
            QGraphicsView.FullViewportUpdate
        )

        self.setDragMode(
            QGraphicsView.RubberBandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setFrameShape(QGraphicsView.NoFrame)

        self.setAcceptDrops(True)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self._middle_pressed = False
        self._last_pos = QPoint()
        self.package = None

    # --------------------------------------------------------

    def set_package(self, package):

        self.package = package

    # --------------------------------------------------------

    def dragEnterEvent(self, event):

        if self._has_piece(event.mimeData()):
            event.acceptProposedAction()
            return

        super().dragEnterEvent(event)

    # --------------------------------------------------------

    def dragMoveEvent(self, event):

        if self._has_piece(event.mimeData()):
            event.acceptProposedAction()
            return

        super().dragMoveEvent(event)

    # --------------------------------------------------------

    def dropEvent(self, event):

        piece_name = self._piece_name_from_mime(event.mimeData())

        if not piece_name or self.package is None:
            super().dropEvent(event)
            return

        piece = self.package.get(piece_name)

        if piece is None:
            super().dropEvent(event)
            return

        scene_pos = self.mapToScene(event.position().toPoint())
        snapped_pos = self._snap_to_grid(scene_pos)

        item = PieceGraphicsItem(piece)
        item.setPos(snapped_pos)

        self.scene.addItem(item)

        event.acceptProposedAction()

    # --------------------------------------------------------

    def _has_piece(self, mime_data):

        return (
            self.package is not None and
            self._piece_name_from_mime(mime_data) in self.package.pieces
        )

    # --------------------------------------------------------

    def _piece_name_from_mime(self, mime_data):

        if mime_data.hasFormat(PIECE_MIME_TYPE):
            return bytes(mime_data.data(PIECE_MIME_TYPE)).decode("utf-8")

        if mime_data.hasText():
            return mime_data.text()

        return None

    # --------------------------------------------------------

    def _snap_to_grid(self, pos):

        grid = WorldScene.GRID_SIZE

        x = round(pos.x() / grid) * grid
        y = round(pos.y() / grid) * grid

        return QPoint(x, y)

    # --------------------------------------------------------

    def wheelEvent(self, event):

        factor = 1.15

        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1 / factor, 1 / factor)

    # --------------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.MiddleButton:

            self._middle_pressed = True

            self._last_pos = event.pos()

            self.setCursor(Qt.ClosedHandCursor)

            event.accept()

            return

        super().mousePressEvent(event)

    # --------------------------------------------------------

    def mouseMoveEvent(self, event):

        if self._middle_pressed:

            delta = event.pos() - self._last_pos

            self._last_pos = event.pos()

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            event.accept()

            return

        super().mouseMoveEvent(event)

    # --------------------------------------------------------

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MiddleButton:

            self._middle_pressed = False

            self.setCursor(Qt.ArrowCursor)

            event.accept()

            return

        super().mouseReleaseEvent(event)
