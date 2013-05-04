# -*- coding:utf-8 -*-
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


class Sansimera_data_gen(sansimera_data.Sansimera_data):
   def __init__(self):
      self.gen_elist=[]


   def parser_gen(self,i):
      ifind=i.index('>')
      i=i[ifind+1:]
      i=i.lstrip()
      if i.count('[Αποφθέγματα]')>=1:
         i=i.replace("[Αποφθέγματα]", " ")
      if i.count('&nbsp;')>=1:
         i=i.replace("&nbsp;", " ")
      if len(i)<=6:
         if i[:-2].isdigit():
            i='\n'+i # Add the title gennisi and a new line below for the event
      if i!='':
         i=i.rstrip()
         self.gen_elist.append(i+' ')


   def genniseis(self):
      self.gen_htmll=''
      try:
         arxeio=open('sansimera_html','r')
         gen_html=arxeio.read()
         self.gen_htmll=gen_html.split('h2')
         self.gen_htmll=self.gen_htmll[4]
         self.gen_htmll=self.gen_htmll.split('<')
         arxeio.close()
      except:
         self.htmll='Eλέγξτε τη σύνδεσή σας.'
         self.gen_elist.append(self.htmll)
      return self.gen_htmll

   def out_genniseis(self):
      start_count=False
      htmll=self.genniseis()
      for i in htmll:
         if i.count('b>')==1:
            start_count=True
         if start_count==True:
            self.parser_gen(i)
         if i.count('/div>')==1:
            start_count=False


   def lista_gen(self):
      flag_empty=False
      self.out_genniseis()
      lista=self.gen_elist[:]
      count_lista=[]
      count=0
      for i in lista:
         if len(i)<=7 and i[len(i)-2:]==': ':
            count_lista.append(count)
         count+=1
      self.gn_elist=[]
      item0=0
      item1=1
      mikos=len(count_lista)
      lmikos=len(lista)
      flag_end=False

      for i in count_lista:
         it0=count_lista[item0]
         if mikos==item1:
            it1=lmikos
            flag_end=True
         if flag_end==False:
            it1=count_lista[item1]
         pedio=''.join(lista[it0:it1])
         self.gn_elist.append(pedio)
         item0+=1
         item1+=1
      if len(self.gn_elist)==0:
         flag_empty=True
         self.gn_elist=self.gen_elist[:]

      if len(self.gn_elist)!=0 and flag_empty==False:
         self.gn1_elist=[]
         for i in self.gn_elist:
            i = '\nΓέννηση'+i
            self.gn1_elist.append(i)

      if flag_empty==True:
         return self.gn_elist
      if flag_empty==False:
         return self.gn1_elist



if __name__ == "__main__":
   a1=Sansimera_data_gen()
   lista=a1.lista_gen()
   for i in lista:
      print(i)





