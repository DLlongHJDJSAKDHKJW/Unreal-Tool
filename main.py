from ue_script_executor_modern.ui_mainwindow import ModernUEScriptExecutor
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernUEScriptExecutor()
    window.show()
    sys.exit(app.exec_()) 