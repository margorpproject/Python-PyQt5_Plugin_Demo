"""
"""

import os, sys, importlib, json
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

WIN_TITLE = 'PyQt5 Plugin Demo'
WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT = [0, 20, 400, 300]
MENU_NAMES = ['&Plugins']

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle(WIN_TITLE)
        self.setGeometry(WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT)
        self.init_menu(MENU_NAMES)
        pass
    def init_menu(self, menu_names):
        self.QMenus = {}
        for menu_name in menu_names:
            menu_name = menu_name.replace('&','')
            qMenu = QMenu(menu_name, self)
            self.menuBar().addMenu(qMenu)
            self.QMenus[menu_name] = qMenu
        self.init_plugins()
    def get_plugin_names(self):
        plugin_names = os.listdir('Plugins')
        return plugin_names
    def init_plugins(self):
        self.plugins = {}
        qMenu = self.QMenus['Plugins']
        plugin_names = self.get_plugin_names()
        for plugin_name in plugin_names:
            qAction = QAction(plugin_name, qMenu)
            qAction.triggered.connect(self.on_click)
            qMenu.addAction(qAction)
            manifest_path = os.path.join('Plugins', plugin_name, 'manifest.json')
            with open(manifest_path, 'r') as f:
                manifest_text = f.read()
            manifest_data = json.loads(manifest_text)
            main_name = manifest_data['name']
            plugin_namespace = '.'.join(['Plugins', plugin_name, main_name])
            plugin = importlib.import_module(plugin_namespace)
            self.plugins[plugin_name] = plugin
    def on_click(self):
        sender_name = self.sender().text()
        if sender_name in self.plugins:
            plugin = self.plugins[sender_name]
            plugin_window = plugin.Window(self)
            plugin_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    status = app.exec_()
    sys.exit(status)
