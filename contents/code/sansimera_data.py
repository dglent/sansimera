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


from bs4 import BeautifulSoup
from urlparse import urljoin
import re
import urllib
import os
import Image
import glob
import sansimera_fetch


class Sansimera_data(object):
    
    def __init__(self):
        fetch = sansimera_fetch.Sansimera_fetch()
        self.sanTitle = '&nbsp;'*10+fetch.monthname()+'<br/>'
        
        for _file in glob.glob('*.jpg'):
            os.remove(_file)
        self.baseurl = 'http://www.sansimera.gr/'
        with open('sansimera_html') as html:
            self.soup = BeautifulSoup(html)
        self.allList = []
        
    def getImage(self, text):
        relativeUrls = re.findall('href="(/[a-zA-Z./_0-9-]+)', text)
        year = re.findall('(<div>[0-9]+</div>)', text)
        if len(relativeUrls) > 0:
            for relurl in relativeUrls:
                text = text.replace(relurl, self.baseurl[:-1]+relurl)
        if len(year) > 0 :
            text = text.replace(year[0], '<b>' + year[0] + ':</b>')
        try:
            iconUrl = re.findall('src="(http://[a-zA-Z./_0-9-]+)', text)[0]
            iconName = os.path.basename(iconUrl)
            urllib.urlretrieve(iconUrl, iconName)
            im = Image.open(iconName)
            newim = im.resize((36,32), Image.ANTIALIAS)
            newim.save(iconName)
            # Convert the url to local name
            newText = text.replace(iconUrl, iconName)
            return newText
        except:
            return text
            
    def events(self):
        listd = self.soup.find_all('div')
        count=0
        for div in listd:
            tag = div.get('class')
            if isinstance(tag, list):
                if len(tag) > 1:
                    # Find the Did You Know ...
                    if tag[0] == 'over' and tag[1] == 'mb10':
                        didYouKnow = (str(listd[count]))
                        # Convert url to local path
                        didYouKnow_url_local = self.getImage(didYouKnow)
                        self.allList.append(str('<br/>' + didYouKnow_url_local))
                    # Find the He Said ...    
                    if tag[0] == 'quote' and tag[1] == 'white':
                        said = ('<br/>' + '&nbsp;'*10 + '<b>Είπε:</b>' + str(listd[count]))
                        whoSaid = str(listd[count+3])
                        # Convert url to local path
                        who_url_local = self.getImage(whoSaid)
                        self.allList.append(said + who_url_local)
                        
                if tag[0] == 'timeline-tab-content':
                    event = listd[count].get('id')
                    if event == 'Deaths':
                        event = self.sanTitle + '<small><i>Θάνατος</i></small>'
                    elif event == 'Births':
                        event = self.sanTitle + '<small><i>Γέννηση</small></i>'
                    else:
                        event = self.sanTitle
                if tag[0] == 'timeline-item' and tag[1] == 'clearfix':
                    eventText = str(listd[count])
                    eventText_url_local = self.getImage(eventText)
                    self.allList.append(str('<br/>' + event+eventText_url_local))
            count += 1
        
    def imeres(self):
        worldlist = [str('&nbsp;'*20 + '<b>Παγκόσμιες Ημέρες</b><br/>')]
        lista = self.soup.find_all('a')
        for tag in lista:
            url = tag.get('href')
            if isinstance(url, str):
                if 'worldays' in url or 'namedays' in url:
                    if 'worldays' in url:
                        day = 'w'
                    elif 'namedays' in url:
                        day = 'n'
                        title = self.sanTitle + '<br/>' + '&nbsp;'*20 + '<b>Εορτολόγιο</b><br/>'
                    tag = str(tag)
                    url = str(url)
                    if 'Εορτολόγιο' in tag or 'Παγκόσμιες Ημέρες' in tag:
                        continue
                    fullUrl = urljoin(self.baseurl, url)
                    tag = tag.replace(url, fullUrl)
                    if day == 'w':
                        worldlist.append('<br/>' + tag + '.')
                    elif day == 'n':
                        tag = '<br>'+title+'</br>'+tag
                        self.allList.append(tag)
        if len(worldlist) > 1:
            worldays = ' '.join(worldlist)
            worldays = '<b/>'+self.sanTitle + '<br/>' + worldays
            self.allList.append(worldays)
                    
    
    def getAll(self):
        self.events()
        self.imeres()
        return self.allList
    
if __name__ == "__main__":
    a1=Sansimera()
    lista = a1.getAll()
    for i in lista:
        print(i)
        raw_input()
