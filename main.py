__author__ = "Süleyman Bozkurt"
__version__ = "1.0.0"
__maintainer__ = "Süleyman Bozkurt"
__email__ = "sbozkurt.mbg@gmail.com"
__date__ = '25.08.2022'
__update__ = '25.08.2022'

import time
import requests
import html
import pandas as pd
from datetime import datetime
import re

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'referer': 'https://scholar.google.com/',
}

def main():

    articleID = '4187968156194932672' # needs to be changed to the article, future version it will be changed!
    numberOfResult = 109 # needs to be changed to the article, future version it will be changed!

    date = datetime.now().strftime("%d.%m.%Y")
    columns = ['Published Date', 'Title', 'Link']
    out_df = pd.DataFrame(columns=columns)
    cache = {}

    for i in range(0, numberOfResult, 10):
        print(f'i : {i}')

        url = f'https://scholar.google.com/scholar?start={i}&hl=en&scisbd=1&as_sdt=2005&sciodt=0,5&cites={articleID}&scipsc='

        req = requests.get(url, headers=headers)

        if 'not a robot' in req.text:
            print('[Banned]')
            # time.sleep(60)
            continue

        num = 1
        for titleList in req.text.split('data-clk-atid="'):
            title = titleList.split('">')[1].split('</')[0]
            if ('<span class' not in title) and ('<meta' not in title):
                title= html.unescape(title)
                link = req.text.split('ontouchstart="gs_evt_dsp(event)">')[num].split('href="')[1].split('"')[0]
                publishedDate = re.findall(r"[0-9]{4,7}", str(req.text.split('/a></h3><div class="gs_a">')[num].split('</')))[0]
                if 'favicon' not in link:
                    print(title)
                    print(link)
                    cache = {
                        'Published Date': int(publishedDate),
                        'Title': str(title),
                        'Link': link,
                    }
                    #out_df = out_df.append(cache, ignore_index=True)
                    out_df = pd.concat([out_df, pd.DataFrame.from_records([cache])])
                num+=1

        time.sleep(10) # not to get ban from the google, each search delay a bit

    out_df.to_excel(f'Output_{articleID}_{date}.xlsx', index=False)

if __name__ == '__main__':
    main()
