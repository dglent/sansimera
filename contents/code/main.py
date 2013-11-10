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

from PyQt4.QtCore import Qt, QObject, QTimer, SIGNAL
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import sansimera_data, sansimera_data_gen, sansimera_data_than, sansimera_fetch


class Sansimera(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.download()
        self.deiktis = 0
        self.timer = QTimer(self)
        self.timer1 = QTimer(self)
        self.setMinimumSize(325.0,125.0)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.label = Plasma.Label(self.applet)
        self.icon = Plasma.IconWidget(self.applet)
        self.icon.setIcon(self.package().path() + "contents/icons/sansimera.png")
        self.connect(self.icon, SIGNAL("clicked()"), self.next_item)
        self.label.setText(self.title())
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
        a9 = sansimera_fetch.Sansimera_fetch()
        self.html = a9.html()
        self.online = a9.online


    def title(self):
        'Shows the title with the date'
        a2 = sansimera_fetch.Sansimera_fetch()
        self.title = a2.monthname()
        self.title = self.trUtf8(self.title)
        return self.title

    def next_item(self):
        self.san_text()
        self.timer.start(40000)
        if self.online == False:
            self.download()


    def connection_next_try(self):
        if self.online == False:
            self.download()


    def san_text(self):
        a3 = sansimera_data.Sansimera_data()
        a4 = sansimera_data_gen.Sansimera_data_gen()
        a5 = sansimera_data_than.Sansimera_data_than()
        self.lista1 = a3.lista()
        self.lista2 = a4.lista_gen()
        self.lista3 = a5.out_thanatoi()
        self.lista = self.lista1+self.lista2+self.lista3
        mikos = len(self.lista)
        self.san_lista = self.lista[self.deiktis]
        self.san_lista = self.trUtf8(self.san_lista)
        self.label.setText(self.title+self.san_lista)
        #self.label.setStyleSheet("background:white; font-weight:normal; color:black;")
        self.deiktis+=1
        if self.deiktis == mikos:
            self.deiktis = 0

def CreateApplet(parent):
    return Sansimera(parent)
