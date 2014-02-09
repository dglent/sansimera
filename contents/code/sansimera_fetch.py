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

import os
import datetime
import subprocess

class Sansimera_fetch(object):
    def __init__(self):
        self.online = False


    def url(self):
        imerominia = str(self.pay()+self.ponth())
        self.url = 'http://www.sansimera.gr/almanac/'+imerominia
        return self.url

    def pay(self):
        imera = str(datetime.date.today()).split('-')
        imera = imera[1:]
        self.pay = imera[1]
        return self.pay


    def ponth(self):
        imera = str(datetime.date.today()).split('-')
        imera = imera[1:]
        self.ponth = imera[0]
        return self.ponth

    def monthname(self):
        dico = {'01': 'Ιανουαρίου', '02': 'Φεβρουαρίου', '03': 'Μαρτίου', '04': 'Απριλίου', '05': 'Μαίου', '06': 'Ιουνίου',\
            '07': 'Ιουλίου', '08': 'Αυγούστου', '09': 'Σεπτεμβρίου', '10': 'Οκτωβρίου', '11': 'Νοεμβρίου', '12': 'Δεκεμβρίου'}
        n = self.ponth()
        self.im = str(' '*10+'...Σαν σήμερα '+self.pay()+' '+dico[n]+'\n')
        return self.im

    def html(self):
        cmd = ['kde4-config', '--localprefix']
        output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        path = output[:-1]+'share/apps/plasma/plasmoids/sansimera'
        os.chdir(path)
        link = self.url()
        onoma='sansimera_html'
        comm = 'wget --timeout=5 --user-agent="KDE Plasmoid" '+link+' -O '+onoma
        self.online = True
        os.system(comm)
        arxeio = open(onoma, 'r')
        ss=arxeio.read()
        if ss == '':
            self.online=False
        arxeio.close()



if __name__ == "__main__":
    a1=Sansimera_fetch()
    lista=a1.html()

