"""
=========================================================
 RoboKitHelp Engine

 Preview Widget

 Renderiza uma Piece utilizando apenas QPainter.
 É reutilizado pelo Tooltip, Inspector e Package.
=========================================================
"""

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtWidgets import QWidget

from core.piece import RectElement


class PreviewWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.piece = None

        self.setMinimumSize(180, 180)

        self.setMaximumSize(180, 180)

    # -------------------------------------------------

    def set_piece(self, piece):

        self.piece = piece

        self.update()

    # -------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        # Fundo
        painter.fillRect(
            self.rect(),
            QColor("#303030")
        )

        # Moldura
        painter.setPen(QPen(QColor("#555555"), 1))
        painter.drawRect(
            self.rect().adjusted(0, 0, -1, -1)
        )

        if self.piece is None:

            painter.setPen(Qt.white)

            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "Nenhuma peça"
            )

            return

        # -----------------------------------------
        # Área destinada ao desenho
        # -----------------------------------------

        preview = QRectF(
            20,
            20,
            140,
            100
        )

        # -----------------------------------------
        # Escala
        # -----------------------------------------

        pw = max(self.piece.width, 1)
        ph = max(self.piece.height, 1)

        scale = min(

            preview.width() / pw,

            preview.height() / ph

        )

        offset_x = preview.left() + (preview.width() - pw * scale) / 2

        offset_y = preview.top() + (preview.height() - ph * scale) / 2

        # -----------------------------------------
        # Render
        # -----------------------------------------

        for element in self.piece:

            if isinstance(element, RectElement):

                painter.setBrush(

                    QBrush(
                        QColor(element.fill)
                    )

                )

                painter.setPen(

                    QPen(
                        QColor(element.border),
                        1
                    )

                )

                x = offset_x + element.x * scale

                y = offset_y + element.y * scale

                w = element.width * scale

                h = element.height * scale

                painter.drawRoundedRect(

                    QRectF(x, y, w, h),

                    element.radius,

                    element.radius

                )

        # -----------------------------------------
        # Informações
        # -----------------------------------------

        painter.setPen(Qt.white)

        font = QFont()

        font.setBold(True)

        painter.setFont(font)

        painter.drawText(

            10,

            140,

            self.piece.name

        )

        font.setBold(False)

        painter.setFont(font)

        painter.drawText(

            10,

            158,

            f"{self.piece.width} x {self.piece.height}"

        )

        painter.drawText(

            10,

            174,

            f"{len(self.piece)} elemento(s)"

        )