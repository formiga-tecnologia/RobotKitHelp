from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView
)


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

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self._middle_pressed = False
        self._last_pos = QPoint()

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