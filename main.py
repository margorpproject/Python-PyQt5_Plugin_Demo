"""
author: margorp
objective: Demonstrate how to use PyQt5 to build a gui application which can allow addition of plugin.
"""

import os, sys, json, importlib
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Settings
VERSION = '1.0.0'
WIN_TITLE = 'Horse Project ' + VERSION
WIN_X = 0
WIN_Y = 20
WIN_W = 600
WIN_H = 400
WIN_QMENU_NAMES = ['&Plugins']
PLUGINS_PARENT_FOLDER_NAME = 'Plugins'

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle(WIN_TITLE)
        self.setGeometry(WIN_X, WIN_Y, WIN_W, WIN_H)
        self.init_menu(WIN_QMENU_NAMES)            
        self.init_plugins(PLUGINS_PARENT_FOLDER_NAME)
    def init_menu(self, qm_names):
        self.qmenus = {}
        for qm_name in qm_names:
            qm = QMenu(qm_name, self)
            self.menuBar().addMenu(qm)
            qm_name = qm_name.replace('&','')
            self.qmenus[qm_name] = qm
    def get_plugin_folder_names(self, plugin_parent_folder_name):
        assert(os.path.isdir(plugin_parent_folder_name), 'Error: no plugin folder %s is found' % plugin_parent_folder_name)
        plugin_folder_names = []
        for plugin_folder_name in os.listdir(plugin_parent_folder_name):
            plugin_folder_path = os.path.join(plugin_parent_folder_name, plugin_folder_name)
            if plugin_folder_name.startswith('__') or not os.path.isdir(plugin_folder_path): continue
            plugin_folder_names.append(plugin_folder_name)
        return plugin_folder_names
    def init_plugins(self, plugin_parent_folder_name):        
        plugin_folder_names = self.get_plugin_folder_names(plugin_parent_folder_name)
        self.plugins = {}
        for plugin_folder_name in plugin_folder_names:
            qm = self.qmenus['Plugins']
            qm.addAction(QAction(plugin_folder_name, self))
            plugin_namespace = '.'.join([plugin_parent_folder_name, plugin_folder_name, 'main'])
            plugin = importlib.import_module(plugin_namespace)
            self.plugins[plugin_folder_name] = plugin        
    def on_click(self):
        sender_name = self.sender().text()
        print(sender_name)
        if sender_name in self.plugins:            
            plugin = self.plugins[sender_name]
            sub_window = plugin.Window(self)
            sub_window.show()
if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
