import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import yuki
import threading
import logging

class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

class AppForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(450, 350)
        self.setWindowTitle("Yukiko")
        self.setWindowIcon(QIcon("assets/yukikoIcon.png"))

        self.applyPlayingBtn = QPushButton("Apply Playing Status", self)
        self.playingTextbox = QLineEdit(self)
        # self.applyPlayingBtn.clicked.connect(self.applyPlayingStatus)

        self.logTextBox = QPlainTextEditLogger(self)

        self.logTextBox.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.INFO)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox.widget)
        self.layout.addWidget(self.playingTextbox)
        self.layout.addWidget(self.applyPlayingBtn)

        self.setLayout(self.layout)

    def applyPlayingStatus(self):
        yuki.changePlayingStatus(self.playingTextbox.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = AppForm()
    t = threading.Thread(target = yuki.runBot, name = "Runs the bot")
    t.daemon = True
    t.start()

    window.show()

sys.exit(app.exec_())