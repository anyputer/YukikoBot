import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtCore import *

import yuki
import threading
import logging
import asyncio

from functools import partial

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        colorDict = {
            "INFO":    "<font color=blue>",
            "ERROR":   "<font color=red>",
            "WARNING": "<font color=darkorange>"
        }
        self.widget.append(
            colorDict.get(record.levelname, "<font color=black>") +
            self.format(record) +
            "</font>"
        )
        # self.widget.append("</span>")
        app.processEvents()

class AppForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(640, 480)
        self.setWindowTitle("Yukiko")
        self.setWindowIcon(QIcon("assets/yukikoIcon.png"))

        self.channelTextBox = QLineEdit(self)
        self.channelTextBox.setPlaceholderText("Channel ID")
        # self.channelTextBox.textChanged.connect(partial(await yuki.start_typing, self.channelTextBox.text()))
        self.msgTextBox = QLineEdit(self)
        self.msgTextBox.setPlaceholderText("Message Content")

        # self.applyPlayingBtn.clicked.connect(self.applyPlayingStatus)
        self.sendMSGButton = QPushButton("Send Message", self)

        self.logTextBox = QTextEditLogger(self)

        self.logTextBox.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.INFO)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logTextBox.widget)

        self.layout.addWidget(self.channelTextBox)
        self.layout.addWidget(self.msgTextBox)

        self.layout.addWidget(self.sendMSGButton)

        self.setLayout(self.layout)

    def applyPlayingStatus(self):
        yuki.changePlayingStatus(self.playingTextbox.text())

class RedirToLogger(object):
    # https://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/

    def __init__(self, logger, log_level = logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

if __name__ == "__main__":
    """stdout_logger = logging.getLogger("STDOUT")
    sl = RedirToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
    """

    stderr_logger = logging.getLogger("STDERR")
    sl = RedirToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    app = QApplication(sys.argv)

    # app.setStyle("Fusion")

    window = AppForm()
    t = threading.Thread(target = yuki.run_bot, name = "Runs the bot")
    t.daemon = True
    t.start()

    window.show()

sys.exit(app.exec_())