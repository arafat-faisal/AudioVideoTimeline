# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeLine.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QScrollArea, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget, QPushButton, QSlider) # Added QPushButton and QSlider

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600) # Increased size for better visibility
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # Top section for audio controls and main transcription display
        self.topWidget = QWidget(self.centralwidget)
        self.topWidget.setObjectName(u"topWidget")
        self.verticalLayout_main = QVBoxLayout(self.topWidget)
        self.verticalLayout_main.setSpacing(3)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(10, 10, 10, 10) # Added margins

        # Audio Controls Widget
        self.audioControlWidget = QWidget(self.topWidget)
        self.audioControlWidget.setObjectName(u"audioControlWidget")
        self.horizontalLayout_audio_controls = QHBoxLayout(self.audioControlWidget)
        self.horizontalLayout_audio_controls.setObjectName(u"horizontalLayout_audio_controls")
        self.horizontalLayout_audio_controls.setContentsMargins(0, 0, 0, 0)

        self.playPauseButton = QPushButton(self.audioControlWidget)
        self.playPauseButton.setObjectName(u"playPauseButton")
        self.playPauseButton.setMinimumSize(QSize(40, 40))
        self.playPauseButton.setMaximumSize(QSize(40, 40))
        self.horizontalLayout_audio_controls.addWidget(self.playPauseButton)

        self.currentTimeLabel = QLabel(self.audioControlWidget)
        self.currentTimeLabel.setObjectName(u"currentTimeLabel")
        self.currentTimeLabel.setMinimumSize(QSize(60, 0))
        self.currentTimeLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.horizontalLayout_audio_controls.addWidget(self.currentTimeLabel)

        self.audioSlider = QSlider(self.audioControlWidget)
        self.audioSlider.setObjectName(u"audioSlider")
        self.audioSlider.setOrientation(Qt.Horizontal)
        self.audioSlider.setRange(0, 100) # Initial range, will be updated dynamically
        self.horizontalLayout_audio_controls.addWidget(self.audioSlider)

        self.totalTimeLabel = QLabel(self.audioControlWidget)
        self.totalTimeLabel.setObjectName(u"totalTimeLabel")
        self.totalTimeLabel.setMinimumSize(QSize(60, 0))
        self.totalTimeLabel.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.horizontalLayout_audio_controls.addWidget(self.totalTimeLabel)

        self.verticalLayout_main.addWidget(self.audioControlWidget)

        # Main Transcription Text Browser
        self.transcriptionTextBrowser = QTextBrowser(self.topWidget)
        self.transcriptionTextBrowser.setObjectName(u"transcriptionTextBrowser")
        self.transcriptionTextBrowser.setOpenExternalLinks(True)
        self.transcriptionTextBrowser.setAcceptRichText(True) # Ensure rich text is accepted
        self.verticalLayout_main.addWidget(self.transcriptionTextBrowser)

        self.gridLayout.addWidget(self.topWidget, 0, 0, 1, 1)

        # Bottom section for timeline details (similar to original structure)
        self.bottomWidget = QWidget(self.centralwidget)
        self.bottomWidget.setObjectName(u"bottomWidget")
        self.bottomWidget.setMaximumSize(QSize(16777215, 200)) # Increased height for details
        self.verticalLayout_bottom = QVBoxLayout(self.bottomWidget)
        self.verticalLayout_bottom.setSpacing(3)
        self.verticalLayout_bottom.setObjectName(u"verticalLayout_bottom")
        self.verticalLayout_bottom.setContentsMargins(10, 0, 10, 10)

        # Tracks Widget (Original widget)
        self.widget = QWidget(self.bottomWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 25))
        self.widget.setMaximumSize(QSize(16777215, 100)) # Keep original max size for now
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(20, 0))
        self.widget_5.setMaximumSize(QSize(40, 16777215))
        self.gridLayout_2 = QGridLayout(self.widget_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget_5)
        self.label.setObjectName(u"label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName(u"widget_6")
        self.gridLayout_5 = QGridLayout(self.widget_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        
        # Add Track Button
        self.addTrackButton = QPushButton(self.widget_6)
        self.addTrackButton.setObjectName(u"addTrackButton")
        self.addTrackButton.setMinimumSize(QSize(0, 25))
        self.addTrackButton.setMaximumSize(QSize(16777215, 30))
        self.gridLayout_5.addWidget(self.addTrackButton, 0, 0, 1, 1) # Placed at row 0, col 0

        self.scrollArea = QScrollArea(self.widget_6)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 681, 98))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_5.addWidget(self.scrollArea, 1, 0, 1, 1) # Moved to row 1, col 0

        self.horizontalLayout.addWidget(self.widget_6)
        self.verticalLayout_bottom.addWidget(self.widget)

        # Sentence+timestamp widget (Original widget)
        self.widget_2 = QWidget(self.bottomWidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 20))
        self.widget_2.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMinimumSize(QSize(20, 0))
        self.widget_7.setMaximumSize(QSize(40, 16777215))
        self.gridLayout_3 = QGridLayout(self.widget_7)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.sentenceTimestampLabel = QLabel(self.widget_7) # Renamed label_2
        self.sentenceTimestampLabel.setObjectName(u"sentenceTimestampLabel")
        self.gridLayout_3.addWidget(self.sentenceTimestampLabel, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.widget_7)

        self.widget_8 = QWidget(self.widget_2)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_2 = QVBoxLayout(self.widget_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_12 = QWidget(self.widget_8)
        self.widget_12.setObjectName(u"widget_12")
        self.gridLayout_8 = QGridLayout(self.widget_12)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_12)
        self.label_5.setObjectName(u"label_5")
        self.gridLayout_8.addWidget(self.label_5, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_12)

        self.widget_11 = QWidget(self.widget_8)
        self.widget_11.setObjectName(u"widget_11")
        self.gridLayout_7 = QGridLayout(self.widget_11)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_11)
        self.label_4.setObjectName(u"label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_11)
        self.horizontalLayout_3.addWidget(self.widget_8)
        self.verticalLayout_bottom.addWidget(self.widget_2)

        # Subtitle-like view with word highlight (Original widget)
        self.widget_3 = QWidget(self.bottomWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(300, 16))
        self.widget_3.setMaximumSize(QSize(16777215, 50)) # Increased height for subtitle
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_9 = QWidget(self.widget_3)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setMinimumSize(QSize(20, 0))
        self.widget_9.setMaximumSize(QSize(40, 16777215))
        self.gridLayout_4 = QGridLayout(self.widget_9)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.subtitleLabel = QLabel(self.widget_9) # Renamed label_3
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.gridLayout_4.addWidget(self.subtitleLabel, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.widget_9)

        self.wordHighlightTextBrowser = QTextBrowser(self.widget_3) # Renamed textBrowser
        self.wordHighlightTextBrowser.setObjectName(u"wordHighlightTextBrowser")
        self.wordHighlightTextBrowser.setAcceptRichText(True) # Ensure rich text is accepted
        self.horizontalLayout_2.addWidget(self.wordHighlightTextBrowser)
        self.verticalLayout_bottom.addWidget(self.widget_3)


        self.gridLayout.addWidget(self.bottomWidget, 1, 0, 1, 1) # Moved bottomWidget to row 1

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Audio Timeline Viewer", None))
        self.playPauseButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.currentTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.totalTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Tracks", None))
        self.addTrackButton.setText(QCoreApplication.translate("MainWindow", u"Add New Track", None)) # Set button text
        self.sentenceTimestampLabel.setText(QCoreApplication.translate("MainWindow", u"Sentence+timestamp", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"sentences", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"timestamps", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"subtitle like view with word highlight", None))
    # retranslateUi

