from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QLabel, QWidget, QShortcut, QProgressBar, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QValidator, QKeySequence

class StatusBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.bg_color("white", "black")
        self.hbox = QHBoxLayout(self)
        self.hbox.setObjectName("status_hbox")
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        self.cmd = StatusCommand(self)
        self.hbox.addWidget(self.cmd)

        self.lbl = StatusText(self)
        self.hbox.addWidget(self.lbl)

        self.prog = StatusProgress(self)
        self.hbox.addWidget(self.prog)

    def bg_color(self, fg, bg):
        self.setStyleSheet("""
            * {
                background: """ + bg + """;
                color: """ + fg + """;
                font-family: Monospace, Courier;
            }""")

    def disp_error(self, text):
        self.bg_color('white', 'red')
        self.lbl.setText('Error: {}'.format(text))

class StatusProgress(QProgressBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        #self.setStyleSheet("padding-right: 1px")
        self.hide()

    # FIXME this size foo doesn't work right.
    # Maybe here we should just reimplement the drawing part.

    def minimumSizeHint(self):
        status_size = parent.size()
        return QSize(20, status_size.height())

    def sizeHint(self):
        return minimumSizeHint()

    def set_progress(self, prog):
        self.show()
        self.setValue(prog)

class StatusText(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet("padding-right: 1px")

class StatusCommand(QLineEdit):
    got_cmd = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet("border: 0px; padding-left: 1px")
        self.setValidator(CmdValidator())
        self.returnPressed.connect(self.process_cmd)

        # FIXME this only works with real esc key, not with xmodmapped
        self.esc = QShortcut(self)
        self.esc.setKey(QKeySequence(Qt.Key_Escape))
        self.esc.setContext(Qt.WidgetWithChildrenShortcut)
        self.esc.activated.connect(parent.setFocus)

    def process_cmd(self):
        text = self.text().lstrip(':')
        self.setText('')
        self.got_cmd.emit(text)

    def set_cmd(self, text):
        self.setText(text)
        self.setFocus()

    def focusOutEvent(self, event):
        self.setText('')
        super().focusOutEvent(event)

class CmdValidator(QValidator):
    def validate(self, string, pos):
        if string.startswith(':'):
            return (QValidator.Acceptable, string, pos)
        else:
            return (QValidator.Invalid, string, pos)
