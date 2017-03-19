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
    shutil.copy(clippings, clippings_path)
    
    def __init__(self, journal):

        self.journal = journal

    def run(self):
        
        with open(self.clippings_path, 'r') as f:
            everything = f.read()

        everything = everything.replace('\ufeff', '')
        sections = everything.split('==========\n')

        print(len(sections))
        for clip in sections:

            data = clip.split('\n')

            print(data[3])

            br0 = [i for i, x in enumerate(data[0]) if x == '('][-1]
            book_title = data[0][:br0]
            # author = data[0][br0+1:-1]

            meta_info = data[1].split('|')
            page = meta_info[0][meta_info[0].find('p') + 5:-1]
            # location = 

            br1 = meta_info[2].find(',')
            entry_date = datetime.datetime.strptime(meta_info[2][br1+2:], '%B %d, %Y %I:%M:%S %p').strftime("%Y-%m-%d %H:%M:%S")
            # entry_date = datetime.datetime.strptime(meta_info[2][br1+2:-11], '%B %d, %Y').strftime("%Y-%m-%d")
            content = data[3]

            # bcmd = "dayone2 -j {0} --date={1} new {2} --tags {3} {4}".format(self.journal, 
            #                                                         entry_date, 
            #                                                         content,
            #                                                         book_title,
            #                                                         author)
            bcmd = "dayone2 -j {0} --date={1} new {2} --tags {3}".format(self.journal, 
                                                                    re.escape(entry_date), 
                                                                    re.escape(content),
                                                                    re.escape(book_title),
                                                                    )
            subprocess.Popen(bcmd, shell=True)



if __name__ == "__main__":

    journal = sys.argv[1]
    k = k2d(journal)
    k.run()