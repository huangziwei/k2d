#!/usr/bin/env python3

import os
import re
import sys
import shutil
import subprocess
import datetime

class k2d:


    home_dir = os.path.expanduser('~')
    save_dir = home_dir + '/Documents/k2d'

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    clippings = '/Volumes/Kindle/documents/My Clippings.txt'
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    clippings_path = save_dir + '/My_Clippings_{}.txt'.format(timestamp)
    try:
        shutil.move(clippings, clippings_path)
    except FileNotFoundError:
        print('Cannot find the file \'My Clippings.txt\' in your Kindle!')
        sys.exit(0)
    # shutil.copy(clippings, clippings_path)
    
    def __init__(self, journal):

        self.journal = journal

    def _get_meta(self, data):


        meta0 = data[0]
        br_pts0 = [i for i, x in enumerate(meta0) if x == '(']
        if len(br_pts0) == 0:
            book_title = meta0
            author = 'Unknown'
        else:
            br0 = br_pts0[-1]
            book_title = meta0[:br0]
            author = meta0[br0+1:-1]

            if ',' in author:
                parts = author.split(',')
                author = parts[1][1:] + ' ' + parts[0]

            if ';' in author:
                author = author.split(';')

        meta1 = data[1].split('|')
        if len(meta1) == 3:
            num_pages = meta1[0][meta1[0].find('p') + 5:-1]
            location = meta1[1][1:-1]
            br1 = meta1[2].find(',')
            entry_date = datetime.datetime.strptime(meta1[2][br1+2:], '%B %d, %Y %I:%M:%S %p').strftime("%Y-%m-%d %H:%M:%S")
        elif len(meta1) == 2:
            num_pages = 'Unknown'
            location = meta1[0][meta1[0].find('on') + 3:-1]
            br1 = meta1[1].find(',')
            entry_date = datetime.datetime.strptime(meta1[1][br1+2:], '%B %d, %Y %I:%M:%S %p').strftime("%Y-%m-%d %H:%M:%S")
        


        return {
                'book_title': book_title,
                'author': author,
                'num_pages': num_pages,
                'location': location,
                'entry_date': entry_date
            }

    def run(self):
        
        with open(self.clippings_path, 'r') as f:
            everything = f.read()

        everything = everything.replace('\ufeff', '')
        sections = everything.split('==========\n')

        print("Importing {} highlight(s):\n".format(len(sections)) )

        for i, clip in enumerate(sections[:-1]):

            data = clip.split('\n')


            meta_info = self._get_meta(data)

            footer = '\n\n(Page {} / {})'.format(meta_info['num_pages'], meta_info['location'])
            content = data[3] + footer

            with open('tmp.txt', 'w') as f:
                f.write(content)
            
            print('\n({:02d}/{:02d}) Importing a clip from {}.\n'.format(i, len(sections)-1, meta_info['book_title']))
            print('\t' + content)
            
            cmd0 = 'dayone2 '
            cmd1 = '-j {} '.format(self.journal)
            cmd2 = '--date={} '.format(re.escape(meta_info['entry_date']))
            cmd3 = 'new < {} '.format('tmp.txt')
            cmd4 = '--tags ' + re.escape(meta_info['book_title']) + ' '
            
            if type(meta_info['author']) is str:
                cmd5 = re.escape(meta_info['author'])
            else:
                cmd5 = ''
                for i, a in enumerate(meta_info['author']):
                    print(a)
                    cmd5 += '{} '.format(re.escape(a)) + ' '
                # cmd5 = re.escape(cmd5)

            bcmd = cmd0 + cmd1 + cmd2 + cmd3 + cmd4 + cmd5

            subprocess.call(bcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.remove('tmp.txt')

if __name__ == "__main__":

    journal = sys.argv[1]
    k = k2d(journal)
    k.run()
    print('\nDONE!')
