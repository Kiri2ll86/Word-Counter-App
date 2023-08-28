import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
import re
from collections import Counter
import pymorphy2

class WordCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Приложение «Счетчик слов»')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_area1 = QTextEdit()
        self.text_area2 = QTextEdit()
        self.result_button = QPushButton('Посчитать слова')

        self.result_button.clicked.connect(self.count_words)

        layout.addWidget(self.text_area1)
        layout.addWidget(self.result_button)
        layout.addWidget(self.text_area2)
        
        central_widget.setLayout(layout)

        self.morph = pymorphy2.MorphAnalyzer()

    def normalize_word(self, word):
        parsed_word = self.morph.parse(word)[0]
        normalized_form = parsed_word.normal_form
        return normalized_form

    def count_words(self):
        text = self.text_area1.toPlainText()
        # words = text.lower().split()
        words = re.findall(r'\b\w{3,}\b', text.lower())  # Используем re для извлечения слов длиной не менее трех букв
        normalized_words = [self.normalize_word(word) for word in words]

        word_counts = Counter(normalized_words)
        most_common, least_common = word_counts.most_common(1)[0], word_counts.most_common()[-1]

        result_text = f"<b>Чаще всего:</b> {most_common[0]} - {most_common[1]} раз<br>"
        result_text += f"<b>Реже всего:</b> {least_common[0]}"

        self.text_area2.setHtml(result_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WordCounterApp()
    window.show()
    sys.exit(app.exec_())
