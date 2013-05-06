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

import sansimera_data
import re


class Sansimera_data_than(sansimera_data.Sansimera_data):
    def __init__(self):
        self.than_elist = []

    def parser_than(self,i):
        text = True
        try:
            ifind = i.index('</b>')
        except:
            text=False

        if text == True:
            i = i.lstrip()
            sfind = i.index('</small>')
            i = i.replace(i[sfind:],"")

        i = re.sub('<[^>]+>', '', i)
        if i.count('[Αποφθέγματα]') >= 1:
            i = i.replace("[Αποφθέγματα]", " ")
        if i.count('&nbsp;') >= 1:
            i = i.replace("&nbsp;", " ")
        if i.count('&rsquo;') >= 1:
            i = i.replace("&rsquo;", "'")
        i='\n'+i
        if i != '':
            i = i.rstrip()
            self.than_elist.append('\nΘάνατος'+i+'\n')

    def thanatoi(self):
        try:
            html_file = open('sansimera_html','r')
            than_html = html_file.read()
            self.than_htmll = than_html.split('h2')
            self.than_htmll = self.than_htmll[6]
            self.than_htmll = self.than_htmll.split("contxtad")
            self.than_htmll = self.than_htmll[0]
            self.than_htmll = self.than_htmll.split("<div class='data_row clear fleft'>")
            html_file.close()
        except:
            self.htmll = 'Δεν βρέθηκαν γεγονότα.'
            self.than_elist.append(self.htmll)
        return self.than_htmll

    def out_thanatoi(self):
        start_count = False
        htmll = self.thanatoi()
        count = 0
        keim = ''.join(htmll)
        htmll = keim.split('<b>')
        # Find the text with year
        pattern = '^[0-9]+: </b>'
        regexp = re.compile(pattern)
        for i in htmll:
            result = regexp.search(i)
            if result:
                # Send the text with the year to the parser
                self.parser_than(i)

        return self.than_elist

if __name__ == "__main__":
    a1=Sansimera_data_than()
    lista = a1.out_thanatoi()
    for i in a1.than_elist:
        print(i)
