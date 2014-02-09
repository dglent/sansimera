# -*- coding: utf-8 -*-
# Copyright (C) 2013  Dimitrios Glentadakis <dglent@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import *
from PyKDE4 import plasmascript
from PyQt4 import uic
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
import sansimera_data
import sansimera_fetch



class Sansimera(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):

        self.fonts = self.config().readEntry("blackfonts", False).toBool()
        self.setHasConfigurationInterface(True)
        self.download()
        data = sansimera_data.Sansimera_data()
        self.lista = data.getAll()
        self.deiktis = 0
        self.timer = QTimer(self)
        self.timer1 = QTimer(self)
        self.setMinimumSize(325.0,125.0)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.label = Plasma.TextBrowser(self.applet)
        #self.label = Plasma.Label(self.applet)
        self.icon = Plasma.IconWidget(self.applet)
        self.icon.setIcon(self.package().path() + "contents/icons/sansimera.png")
        self.icon_path = (self.package().path() + "contents/icons/sansimera.png")
        self.connect(self.icon, SIGNAL("clicked()"), self.next_item)
        firstTitleInit = sansimera_fetch.Sansimera_fetch()
        firstTitle = firstTitleInit.monthname()
        
        self.label.setText(firstTitle)
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.layout.addItem(self.label)
        self.setLayout(self.layout)

        self.san_text()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.san_text)
        self.timer.start(40000)
        QObject.connect(self.timer1, SIGNAL("timeout()"), self.connection_next_try)
        self.timer1.start(1200000)
        

    def download(self):
        fetch = sansimera_fetch.Sansimera_fetch()
        self.html = fetch.html()
        self.online = fetch.online

    def next_item(self):
        self.san_text()
        self.timer.start(40000)
        if self.online == False:
            self.download()


    def connection_next_try(self):
        if self.online == False:
            self.download()


    def san_text(self):
        mikos = len(self.lista)
        self.san_lista = self.lista[self.deiktis]
        self.san_lista = self.trUtf8(self.san_lista)
        self.apply_settings()
        self.label.setText(self.san_lista)
        #self.label.setStyleSheet("background:white; font-weight:normal; color:black;")
        self.deiktis+=1
        if self.deiktis == mikos:
            self.deiktis = 0

    def createConfigurationInterface(self, parent):
        self.general_widget = QWidget(parent)
        parent.okClicked.connect(self.ConfigAccepted)
        parent.applyClicked.connect(self.ConfigAccepted)
        parent.cancelClicked.connect(self.configWidgetDestroyed)
        self.general_ui = uic.loadUi(self.package().filePath('ui','general.ui'), self.general_widget)
        self.general_ui.blackfonts_checkBox.setChecked(self.config().readEntry("blackfonts", False ).toBool())
        self.general_ui.blackfonts_checkBox.stateChanged.connect(parent.settingsModified)
        parent.addPage(self.general_widget, i18n('General'), self.icon_path)
        
    def ConfigAccepted(self):
        self.config().writeEntry("blackfonts", bool(self.general_ui.blackfonts_checkBox.isChecked()))
        self.fonts = self.general_ui.blackfonts_checkBox.isChecked()
        self.apply_settings()
        
    def configWidgetDestroyed(self):
        self.general_widget = None
        self.general_ui = None
        
    def apply_settings(self):
        if self.fonts:
            self.label.setStyleSheet("color:black;")
            self.label.setText(self.san_lista)
        if not self.fonts:
            self.label.setStyleSheet("color:white;")  
            self.label.setText(self.san_lista)
        

def CreateApplet(parent):
    return Sansimera(parent)
