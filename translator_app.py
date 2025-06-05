import sys
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox,
    QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QColor
from PyQt6.QtCore import Qt


class TransparentTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Semi-transparent white background with rounded corners and padding
        self.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                font-size: 14px;
                padding: 8px;
            }
        """)


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Translator - Free Edition")
        self.setGeometry(200, 200, 850, 500)
        self.bg_path = r"C:\Users\Akshay Sai\bg.jpg"
        self.init_ui()

    def init_ui(self):
        # Set background image scaled to window size
        self.setAutoFillBackground(True)
        self.update_background()

        # Input and Output Text Edits with transparency
        self.input_text = TransparentTextEdit()
        self.output_text = TransparentTextEdit()
        self.output_text.setReadOnly(True)

        # Fixed reasonable size
        self.input_text.setFixedHeight(180)
        self.output_text.setFixedHeight(180)

        # Labels for inputs with white text and shadow effect for readability
        label_style = """
            color: white;
            font-weight: bold;
            font-size: 16px;
            text-shadow: 1px 1px 2px black;
        """

        self.input_label = QLabel("Input Text:")
        self.input_label.setStyleSheet(label_style)
        self.output_label = QLabel("Translated Output:")
        self.output_label.setStyleSheet(label_style)

        # Language selection dropdown
        self.lang_label = QLabel("Select Target Language:")
        self.lang_label.setStyleSheet(label_style)

        self.lang_box = QComboBox()
        self.languages = {
            "English (en)": "en", "Hindi (hi)": "hi", "Telugu (te)": "te",
            "Spanish (es)": "es", "French (fr)": "fr", "German (de)": "de",
            "Tamil (ta)": "ta", "Kannada (kn)": "kn"
        }
        self.lang_box.addItems(self.languages.keys())
        self.lang_box.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 200);
                font-size: 14px;
                border-radius: 8px;
                padding: 4px;
                min-width: 150px;
            }
        """)

        # Buttons with nice blue style
        button_style = """
            QPushButton {
                background-color: #3a86ff;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #265dff;
            }
            QPushButton:pressed {
                background-color: #1a44cc;
            }
        """

        self.translate_button = QPushButton("Translate")
        self.translate_button.setStyleSheet(button_style)
        self.translate_button.clicked.connect(self.translate_text)

        self.speak_button = QPushButton("Speak Input")
        self.speak_button.setStyleSheet(button_style)
        self.speak_button.clicked.connect(self.speech_to_text)

        self.play_button = QPushButton("Speak Output")
        self.play_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.speak_output)

        # Layouts setup

        # Top labels side by side
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(self.input_label)
        labels_layout.addStretch()
        labels_layout.addWidget(self.output_label)
        labels_layout.setContentsMargins(10, 10, 10, 0)

        # Text areas side by side
        texts_layout = QHBoxLayout()
        texts_layout.addWidget(self.input_text)
        texts_layout.addWidget(self.output_text)
        texts_layout.setContentsMargins(10, 0, 10, 0)
        texts_layout.setSpacing(30)

        # Controls (language dropdown + buttons)
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.lang_label)
        controls_layout.addWidget(self.lang_box)
        controls_layout.addStretch()
        controls_layout.addWidget(self.translate_button)
        controls_layout.addWidget(self.speak_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.setSpacing(20)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(texts_layout)
        main_layout.addLayout(controls_layout)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(main_layout)

    def update_background(self):
        palette = QPalette()
        pixmap = QPixmap(self.bg_path)
        if pixmap.isNull():
            print(f"Warning: Background image not found at {self.bg_path}")
            self.setStyleSheet("background-color: #222222;")  # fallback color
            return
        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def translate_text(self):
        source = self.input_text.toPlainText()
        target_lang = self.languages[self.lang_box.currentText()]
        if source.strip():
            try:
                translated = GoogleTranslator(source='auto', target=target_lang).translate(source)
                self.output_text.setPlainText(translated)
            except Exception as e:
                self.output_text.setPlainText(f"Error: {e}")
        else:
            self.output_text.setPlainText("Please enter text to translate.")

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.input_text.setPlainText("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.input_text.setPlainText(text)
            except sr.UnknownValueError:
                self.input_text.setPlainText("Could not understand audio.")
            except sr.RequestError:
                self.input_text.setPlainText("Check your internet connection.")
            except Exception as e:
                self.input_text.setPlainText(str(e))

    def speak_output(self):
        text = self.output_text.toPlainText()
        if text.strip():
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec())
