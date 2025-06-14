from PySide6.QtWidgets import QWidget, QToolTip
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRectF, Signal

class TimelineTrackWidget(QWidget):
    # Signal to notify parent when user scrubs timeline
    scrubbed = Signal(float)

    def __init__(self, segments, total_duration, parent=None):
        super().__init__(parent)
        self.segments = segments
        self.total_duration = total_duration
        self.current_time = 0.0
        self.zoom = 1.0
        self.setMinimumHeight(60)
        self.setMouseTracking(True)
        self.setToolTip("Click or drag to scrub. Hover over blocks for info.")

    def set_current_time(self, t):
        self.current_time = t
        self.update()

    def set_zoom(self, z):
        self.zoom = z
        self.update()

    def set_segments(self, segments):
        self.segments = segments
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        h = self.height()
        w = self.width()
        painter.fillRect(self.rect(), QColor("#444444"))

        if self.total_duration <= 0:
            painter.end()
            return

        # Draw segments as blocks
        for seg in self.segments:
            x = seg['start'] / self.total_duration * w * self.zoom
            width = max(2, (seg['end'] - seg['start']) / self.total_duration * w * self.zoom)
            rect = QRectF(x, 10, width, h-20)
            painter.setBrush(QColor("#61c33c"))
            painter.setPen(QColor("#333"))
            painter.drawRect(rect)

            # Optional: Draw text in segment
            painter.setPen(QColor("#fff"))
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            text = seg.get('text', '')
            painter.drawText(rect.adjusted(2,2,-2,-2), Qt.AlignLeft|Qt.AlignTop, text[:30])

        # Draw playhead
        playhead_x = self.current_time / self.total_duration * w * self.zoom
        painter.setPen(QPen(QColor("#00FFFF"), 2))
        painter.drawLine(playhead_x, 0, playhead_x, h)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            t = (event.x() / (self.width() * self.zoom)) * self.total_duration
            self.scrubbed.emit(max(0.0, min(self.total_duration, t)))

    def mouseMoveEvent(self, event):
        w = self.width()
        for seg in self.segments:
            x = seg['start'] / self.total_duration * w * self.zoom
            width = max(2, (seg['end'] - seg['start']) / self.total_duration * w * self.zoom)
            rect = QRectF(x, 10, width, self.height()-20)
            if rect.contains(event.pos()):
                QToolTip.showText(event.globalPos(), f"{seg.get('text','')}\n{seg['start']:.2f}s - {seg['end']:.2f}s")
                break
        else:
            QToolTip.hideText()