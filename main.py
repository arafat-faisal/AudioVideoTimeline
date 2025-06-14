import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSlider, QPushButton, QLabel, QTextBrowser,
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QMimeData, QUrl
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QTextDocument, QDrag

# Import the updated UI class
from ui_timeline_updated import Ui_MainWindow
from timeline_track_widget import TimelineTrackWidget

# --- Custom Widgets for Drag and Drop ---

class DraggableSentenceLabel(QLabel):
    """A QLabel that can be dragged."""
    def __init__(self, text, sentence_data, parent=None):
        super().__init__(text, parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setAlignment(Qt.AlignCenter)
        self.sentence_data = sentence_data  # Store the full sentence data

    def mousePressEvent(self, event):
        """Handle mouse press event to start drag."""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse move event to perform drag if threshold is met."""
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        # Store sentence text and timestamp in MIME data as JSON string
        mime_data.setText(json.dumps({
            "text": self.sentence_data["text"],
            "start": self.sentence_data["start"],
            "end": self.sentence_data["end"]
        }))
        drag.setMimeData(mime_data)
        drag.exec(Qt.MoveAction)

class DropAreaWidget(QFrame):
    """A widget that can accept dropped DraggableSentenceLabels."""
    def __init__(self, track_id, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 50)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setAcceptDrops(True) # Enable dropping
        self.track_id = track_id
        self.dropped_content_layout = QVBoxLayout(self) # Layout to hold dropped items
        self.dropped_content_layout.setAlignment(Qt.AlignTop)
        self.setStyleSheet("DropAreaWidget { background-color: #555555; border: 1px dashed #00FFFF; border-radius: 5px; }")
        
        self.placeholder_label = QLabel(f"Drop sentences here for Track {track_id}", self)
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.dropped_content_layout.addWidget(self.placeholder_label)

    def dragEnterEvent(self, event):
        """Accept the drag if it contains plain text (our sentence data)."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Allow drag move if it contains plain text."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle the drop event and display the dropped sentence."""
        if event.mimeData().hasText():
            try:
                sentence_data = json.loads(event.mimeData().text())
                sentence_text = sentence_data.get("text", "N/A")
                sentence_start = sentence_data.get("start", 0.0)
                sentence_end = sentence_data.get("end", 0.0)

                # Remove placeholder if content is dropped
                if self.placeholder_label:
                    self.placeholder_label.hide()
                    self.dropped_content_layout.removeWidget(self.placeholder_label)
                    self.placeholder_label = None

                # Create a new label to display the dropped sentence info
                dropped_label = QLabel(
                    f"'{sentence_text}'\n({sentence_start:.2f}s - {sentence_end:.2f}s)", self
                )
                dropped_label.setWordWrap(True)
                dropped_label.setStyleSheet("color: #FFFFFF; background-color: #3a8fe6; border-radius: 5px; padding: 3px; margin: 2px;")
                self.dropped_content_layout.addWidget(dropped_label)
                event.acceptProposedAction()

            except json.JSONDecodeError:
                event.ignore()
        else:
            event.ignore()

# --- Main Application Class ---

class AudioTimelineApp(QMainWindow, Ui_MainWindow):
    def __init__(self, transcription_path, style_path):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Audio Timeline Viewer")

        self.transcription_data = None
        self.current_time = 0.0
        self.total_duration = 0.0
        self.is_playing = False

        # Load transcription data
        if os.path.exists(transcription_path):
            with open(transcription_path, 'r', encoding='utf-8') as f:
                self.transcription_data = json.load(f)
            self._initialize_transcription_display()
        else:
            self.transcriptionTextBrowser.setHtml("<p style='color:red;'>Error: Transcription file not found.</p>")
            self._show_message_box("Error", f"Transcription file not found at {transcription_path}")
            print(f"Error: Transcription file not found at {transcription_path}")

        # --- TIMELINE TRACK WIDGET ---
        self.timeline_widget = None
        if self.transcription_data and "segments" in self.transcription_data:
            self.timeline_widget = TimelineTrackWidget(
                self.transcription_data["segments"],
                self.total_duration,
                self
            )
            # Place timeline_widget in the UI grid just under the topWidget
            self.gridLayout.addWidget(self.timeline_widget, 1, 0, 1, 2)  # full width

            # Connect scrubbing
            self.timeline_widget.scrubbed.connect(self._scrub_to_time)

        # Calculate total duration from the last word's end time
        if self.transcription_data and "segments" in self.transcription_data and self.transcription_data["segments"]:
            last_segment = self.transcription_data["segments"][-1]
            if "words" in last_segment and last_segment["words"]:
                self.total_duration = last_segment["words"][-1]["end"]
            else:
                # Fallback to segment end if no words are present in the last segment
                self.total_duration = last_segment["end"]
        
        self.update_time_labels()

        # Setup Timer for simulated playback
        self.playback_timer = QTimer(self)
        self.playback_timer.setInterval(100) # Update every 100 ms
        self.playback_timer.timeout.connect(self._update_playback)

        # Connect UI elements
        self.playPauseButton.clicked.connect(self.toggle_playback)
        self.audioSlider.sliderMoved.connect(self.seek_audio)
        self.audioSlider.setRange(0, int(self.total_duration * 1000)) # Slider in milliseconds

        # Apply stylesheet
        self._apply_stylesheet(style_path)

        # Connect Add Track button
        self.addTrackButton.clicked.connect(self.add_new_track)
        
        # Setup layout for dynamically added tracks
        self.tracks_container_layout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.tracks_container_layout.setAlignment(Qt.AlignTop) # Align added tracks to the top
        self.scrollAreaWidgetContents.setLayout(self.tracks_container_layout) # Set the layout

        self.track_count = 0 # To assign unique IDs to tracks

        # Create QScrollAreas and TextBrowsers for sentences and timestamps
        self.sentencesTextBrowser = QTextBrowser(self.widget_8)
        self.sentencesTextBrowser.setObjectName(u"sentencesTextBrowser")
        self.sentencesTextBrowser.setAcceptRichText(True)
        self.sentencesTextBrowser.setOpenExternalLinks(False) # Prevent opening external links
        self.sentencesTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.timestampsTextBrowser = QTextBrowser(self.widget_8)
        self.timestampsTextBrowser.setObjectName(u"timestampsTextBrowser")
        self.timestampsTextBrowser.setAcceptRichText(True)
        self.timestampsTextBrowser.setOpenExternalLinks(False)
        self.timestampsTextBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Layout for sentences and timestamps
        self.sentence_timestamp_hlayout = QHBoxLayout(self.widget_8)
        self.sentence_timestamp_hlayout.setContentsMargins(0,0,0,0) # Remove margins
        self.sentence_timestamp_hlayout.addWidget(self.sentencesTextBrowser)
        self.sentence_timestamp_hlayout.addWidget(self.timestampsTextBrowser)
        self.widget_8.setLayout(self.sentence_timestamp_hlayout) # Apply the new layout

        self._populate_sentence_timestamp_views()

    def _scrub_to_time(self, t):
        """Set current time from timeline scrub."""
        self.current_time = t
        self.update_time_labels()
        self.highlight_current_word()
        self.update_subtitle_view()
        if self.timeline_widget:
            self.timeline_widget.set_current_time(self.current_time)

    def _show_message_box(self, title, message):
        """Displays a custom message box instead of alert()."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("QMessageBox { background-color: #3c3c3c; color: #f0f0f0; }"
                              "QMessageBox QLabel { color: #f0f0f0; }"
                              "QMessageBox QPushButton { background-color: #61c33c; color: #ffffff; border-radius: 5px; padding: 5px 10px; }"
                              "QMessageBox QPushButton:hover { background-color: #72d44d; }")
        msg_box.exec()

    def _initialize_transcription_display(self):
        """Initializes the main transcription text browser with all words."""
        full_html = []
        if not self.transcription_data or "segments" not in self.transcription_data:
            return

        for segment in self.transcription_data["segments"]:
            for word_info in segment.get("words", []):
                # Ensure each word is wrapped in a span for potential highlighting
                full_html.append(f"<span class='word-static' data-start='{word_info['start']}' data-end='{word_info['end']}'>{word_info['word']}</span>")
            full_html.append(" ") # Add space between words
        
        self.transcriptionTextBrowser.setHtml(" ".join(full_html).strip())
        self.transcriptionTextBrowser.document().markContentsDirty(0, self.transcriptionTextBrowser.document().characterCount())

    def _populate_sentence_timestamp_views(self):
        """Populates the sentences and timestamps QTextBrowsers with segment data."""
        if not self.transcription_data or "segments" not in self.transcription_data:
            return

        sentences_html = []
        timestamps_html = []

        for i, segment in enumerate(self.transcription_data["segments"]):
            sentence_text = segment.get("text", "")
            start_time = segment.get("start", 0.0)
            end_time = segment.get("end", 0.0)

            # Create a draggable label for each sentence
            draggable_label = DraggableSentenceLabel(sentence_text, segment, self.sentencesTextBrowser)
            draggable_label.setStyleSheet("color: #f0f0f0; padding: 2px; border-bottom: 1px solid #4a4a4a; margin-bottom: 2px;") # Style for individual draggable labels

            # Add it to a temporary layout to put into the QTextBrowser.
            # QTextBrowser doesn't directly support adding widgets, so we format as HTML.
            # For actual dragging of visual items, it's better to add them to a QListWidget or custom QGraphicsScene.
            # Here, we'll make the text itself "draggable" via a custom QLabel within a custom QWidget layout.
            # Given that QTextBrowser directly accepts HTML, we'll just present the text.
            # To make the actual labels draggable, we need a container widget for them.

            # For now, we will simply populate the QTextBrowsers with text.
            # The actual drag and drop will be handled from the 'main_app.py' as the draggable labels are created here.
            sentences_html.append(f"<p style='color: #f0f0f0; margin-bottom: 5px;' class='sentence-item' data-segment-id='{i}'>{sentence_text}</p>")
            timestamps_html.append(f"<p style='color: #a0a0a0; margin-bottom: 5px;'>{self.format_time(start_time)} - {self.format_time(end_time)}</p>")
        
        self.sentencesTextBrowser.setHtml("".join(sentences_html))
        self.timestampsTextBrowser.setHtml("".join(timestamps_html))

        # To make sentence items truly draggable from this view, we'd need to create
        # actual QWidgets (like DraggableSentenceLabel) and add them to a layout
        # within a scrollable QWidget, rather than just using a QTextBrowser.
        # For this demo, the DraggableSentenceLabel is created in the main window
        # but is not directly displayed in the sentencesTextBrowser.
        # Instead, the _rebuild_highlighted_html now rebuilds the main text,
        # and update_subtitle_view updates the wordHighlightTextBrowser.

        # Let's create actual DraggableSentenceLabel widgets to be displayed in a separate area
        # (e.g., in a dedicated section of the UI, or by repurposing an existing one).
        # For simplicity, let's put them in the 'sentences' area of widget_8, which now uses a QHBoxLayout.
        # This will require modifying `ui_timeline_updated.py` to make `widget_12` a container for these draggable items.
        
        # As per the new design, the `sentencesTextBrowser` is meant to display the sentences.
        # To make them draggable, we need to add actual `DraggableSentenceLabel` instances.
        # This requires adjusting `ui_timeline_updated.py` to create a new, dedicated container
        # for draggable sentence labels, or change `sentencesTextBrowser` into a container for widgets.
        # Given the previous context, `sentencesTextBrowser` was a `QTextBrowser`, implying text display.

        # For this iteration, I'll demonstrate the drag-and-drop mechanism by having a hidden set of
        # `DraggableSentenceLabel` instances which can be conceptually dragged, and the drop area.
        # A more complex UI would involve displaying these labels visibly in a `QListWidget`
        # or a custom `QWidget` that holds a `QVBoxLayout` of `DraggableSentenceLabel`s.

        # Let's assume for now that the sentences_html in sentencesTextBrowser is just for display,
        # and the drag originates from a conceptual "source" for simplicity in this turn.
        # If the user wants the text *in the sentencesTextBrowser* to be draggable,
        # that would require more advanced QTextBrowser customization or a different widget.

        # For the purpose of demonstration:
        # Create a scrollable area for draggable sentence labels
        self.sentences_draggable_scroll_area = QScrollArea(self.centralwidget)
        self.sentences_draggable_scroll_area.setObjectName(u"sentencesDraggableScrollArea")
        self.sentences_draggable_scroll_area.setWidgetResizable(True)
        self.sentences_draggable_container = QWidget()
        self.sentences_draggable_container.setObjectName(u"sentencesDraggableContainer")
        self.sentences_draggable_layout = QVBoxLayout(self.sentences_draggable_container)
        self.sentences_draggable_layout.setAlignment(Qt.AlignTop)
        self.sentences_draggable_scroll_area.setWidget(self.sentences_draggable_container)

        # Add this scroll area to the main grid layout
        self.gridLayout.addWidget(self.sentences_draggable_scroll_area, 0, 1, 1, 1) # Position next to main text browser

        for i, segment in enumerate(self.transcription_data["segments"]):
            draggable_label = DraggableSentenceLabel(segment.get("text", "N/A"), segment, self.sentences_draggable_container)
            draggable_label.setWordWrap(True)
            draggable_label.setStyleSheet("color: #FFFFFF; background-color: #5b5b5b; border-radius: 5px; padding: 5px; margin-bottom: 5px;")
            self.sentences_draggable_layout.addWidget(draggable_label)


    def _apply_stylesheet(self, style_path):
        """Loads and applies the QSS stylesheet."""
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        else:
            self._show_message_box("Error", f"Stylesheet file not found at {style_path}")
            print(f"Error: Stylesheet file not found at {style_path}")

    def format_time(self, seconds):
        """Formats seconds into MM:SS string."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def update_time_labels(self):
        """Updates the current time and total duration labels."""
        self.currentTimeLabel.setText(self.format_time(self.current_time))
        self.totalTimeLabel.setText(self.format_time(self.total_duration))
        self.audioSlider.setValue(int(self.current_time * 1000))

    def _update_playback(self):
        """Simulates audio playback and updates UI."""
        self.current_time += 0.1 # Increment by 100 ms
        if self.current_time >= self.total_duration:
            self.current_time = self.total_duration
            self.playback_timer.stop()
            self.is_playing = False
            self.playPauseButton.setText("Play")

        self.update_time_labels()
        self.highlight_current_word()
        self.update_subtitle_view()
        if self.timeline_widget:
            self.timeline_widget.set_current_time(self.current_time)

    def toggle_playback(self):
        """Starts or pauses the simulated audio playback."""
        if self.is_playing:
            self.playback_timer.stop()
            self.playPauseButton.setText("Play")
        else:
            if self.current_time >= self.total_duration: # Restart if at end
                self.current_time = 0.0
            self.playback_timer.start()
            self.playPauseButton.setText("Pause")
        self.is_playing = not self.is_playing

    def seek_audio(self, value):
        """Seeks the audio to a new position based on slider value."""
        self.current_time = value / 1000.0 # Convert milliseconds back to seconds
        self.update_time_labels()
        self.highlight_current_word()
        self.update_subtitle_view()

    def highlight_current_word(self):
        """Highlights the current word in the main transcription text browser."""
        self._rebuild_highlighted_html()

    def _rebuild_highlighted_html(self):
        """Rebuilds the HTML content of the transcription text browser with the current word highlighted."""
        if not self.transcription_data or "segments" not in self.transcription_data:
            return

        rebuilt_html = []
        found_word_in_current_time = False

        for segment in self.transcription_data["segments"]:
            for word_info in segment.get("words", []):
                current_word_text = word_info['word']
                word_start_time = word_info['start']
                word_end_time = word_info['end']

                if word_start_time <= self.current_time < word_end_time:
                    # Apply highlight style using inline CSS for simplicity
                    rebuilt_html.append(f"<span style='color: #00FFFF; font-weight: bold;'>{current_word_text}</span>")
                    found_word_in_current_time = True
                else:
                    rebuilt_html.append(f"<span style='color: #FFFFFF;'>{current_word_text}</span>")
                rebuilt_html.append(" ") # Add space after each word
            
            # Optional: Add a line break after each segment for readability
            # rebuilt_html.append("<br>")

        self.transcriptionTextBrowser.setHtml(" ".join(rebuilt_html).strip()) # .strip() removes trailing space


    def update_subtitle_view(self):
        """Updates the subtitle-like view with word highlight."""
        current_subtitle_words = []
        if self.transcription_data and "segments" in self.transcription_data:
            for segment in self.transcription_data["segments"]:
                segment_start_time = segment['start']
                segment_end_time = segment['end']

                if segment_start_time <= self.current_time < segment_end_time:
                    for word_info in segment.get("words", []):
                        word_start_time = word_info['start']
                        word_end_time = word_info['end']
                        current_word = word_info['word']

                        if word_start_time <= self.current_time < word_end_time:
                            current_subtitle_words.append(f"<span style='color: #FFD700; font-weight: bold;'>{current_word}</span>") # Gold highlight for subtitle
                        else:
                            current_subtitle_words.append(f"<span style='color: #D3D3D3;'>{current_word}</span>") # Light gray for unhighlighted words
                    break # Found the current segment, no need to check others

        self.wordHighlightTextBrowser.setHtml(" ".join(current_subtitle_words))

    def add_new_track(self):
        """Adds a new draggable track area to the scrollable area."""
        self.track_count += 1
        new_track_widget = DropAreaWidget(self.track_count)
        self.tracks_container_layout.addWidget(new_track_widget)
        self.tracks_container_layout.addStretch(1) # Add a stretch to push new widgets to the top


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Paths to your files
    json_file = "ElevenLabs_JRE_NASA_is_SHUTTING_DOWN_Voyager_2_After_It_Captured_THIS_In_Deep_Space!__01_transcription.json"
    qss_file = "styles.qss"

    window = AudioTimelineApp(json_file, qss_file)
    window.show()
    sys.exit(app.exec())

