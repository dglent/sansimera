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


class Sansimera_data(object):
   def __init__(self):
      self.elist=[]

   def parser(self, i):
      ifind=i.index('>')
      i=i[ifind+1:]
      i=i.lstrip()
      if i.count('&nbsp;')>=1:
         i=i.replace("&nbsp;", "")
      if i[0:4].isdigit():
         i='\n'+i
      if i!='':
         i=i.rstrip()
         self.elist.append(i+' ')


   def html(self):
      try:
         arxeio=open('sansimera_html','r')
         html=arxeio.read()
         self.htmll=html.split('h2')
         self.htmll=self.htmll[2]
         self.htmll=self.htmll.split('<')
      except:
         self.htmll='Δεν βρέθηκαν γεγονότα, ελέγξτε τη σύνδεσή σας.'
         self.elist.append(self.htmll)
      return self.htmll



   def out(self):
      start_count=False
      try:
         self.htmll=self.html()
         for i in self.htmll:
            if i.count('b>')==1:
               start_count=True
            if start_count==True:
               self.parser(i)
            if i.count('/div>')==1:
               start_count=False

      except:
         self.elist=['Δεν βρέθηκαν γεγονότα','Ελέγξτε τη σύνδεσή σας']



   def lista(self):
      "Make each event an element of the list"
      self.out()
      self.lista=self.elist[:]
      self.count_lista=[]
      self.sec_lista=[]
      count=0
      #Find the position in the list which containt the year of the events
      for i in self.lista:
         if len(i)==7 and i[5:7]==': ':
            self.count_lista.append(count)
         count+=1

      #Make one element by event in the list
      self.n_elist=[]
      item0=0
      item1=1
      mikos=len(self.count_lista)
      lmikos=len(self.lista)
      flag_end=False

      for i in self.count_lista:
         it0=self.count_lista[item0]
         if mikos==item1:
            it1=lmikos
            flag_end=True
         if flag_end==False:
            it1=self.count_lista[item1]
         pedio=''.join(self.lista[it0:it1])
         self.n_elist.append(pedio)
         item0+=1
         item1+=1
      if len(self.n_elist)==0:
         self.n_elist=self.elist[:]

      return self.n_elist



if __name__ == "__main__":
   a1=Sansimera_data()
   for i in a1.lista():
      print(i)






