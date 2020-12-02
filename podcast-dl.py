#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:36:53 2020

@author: orange
"""

from lxml import etree as ET
import requests
import os

def main():
    
    rssfile = 'al_short.rss'
    #rssfile = 'al_shortest.rss'
    rssfile = 'al.rss'
    tree = ET.parse(rssfile)
    root = tree.getroot()
    nsmap = {'media':'{http://search.yahoo.com/mrss/}'}
    
    # Audioboom RSS feeds list each episode as an <item> tag
    
    podcastElement = root.find('channel').find('title')
    podcastTitle = podcastElement.text
    
    for episode in root.iter('item'):
        
        # find some important informational elements about the episode
        titleElement = episode.find('title')
        mediaElement = episode.find('{http://search.yahoo.com/mrss/}content')
        descrpElement = episode.find('description')
        
        # store that information 
        title = titleElement.text
        url   = mediaElement.get('url')
        urlShort = str(url.split('?',-1)[0]) # get everything before the first '?' in the URL
        descrp = descrpElement.text
        

        # set the download path and filename
        path = '/home/' + os.getlogin() + '/Downloads/' + podcastTitle+'/' + title+'/'
        textfile  = title + '.txt'
        audiofile = title + '.mp3'
        
        # print some information about the current episode
        print()
        print('Podcast: ' + podcastTitle)
        print('Episode: ' + title )
        print('Audio URL: ' + urlShort)
        print('Download path: ' + path)
        print('Descrption: ' + descrp)
        print()
        
        # if the path doesn't exist, make it
        if not os.path.exists(path):
            os.makedirs(path)
            
        # if the text file doesn't exist, make it
        if not os.path.exists(path + textfile):
            # write the above information to a text file
            f = open(path + textfile, "w")
            f.write('Podcast: ' + podcastTitle + '\n\n')
            f.write('Episode: ' + title + '\n\n')
            f.write('Audio URL: ' + urlShort + '\n\n')
            f.write('Download path: ' + path + path + '\n\n')
            f.write('Description: ' + descrp + '\n\n')
            f.close()
        
        # if the audio file doesn't exist, make it
        if not os.path.exists(path + audiofile):

            r = requests.get(urlShort, stream=True)

            # open the file named filename in binary write mode as shorthand fd, 
            # then write each chunk as it comes in to that file.
            with open(path + audiofile, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
    
        
if __name__ == "__main__":
    main();    
