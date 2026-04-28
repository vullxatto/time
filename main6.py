import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, 'domain'))
sys.path.insert(0, os.path.join(root_dir, 'dataaccess'))
sys.path.insert(0, os.path.join(root_dir, 'qt'))
from PyQt5.QtWidgets import QApplication
from mainwindow_ext import mainWindow_ext
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow_ext()
    window.show()
    sys.exit(app.exec_())
