#!/usr/local/bin/python

import urllib
from datetime import date, timedelta

cur_date = date(2007, 2, 8)
step = timedelta(days=7)

def _construct_url(date):
    return 'http://swtychina.com/gb/audiodoc/{year}/{year}{month}/{year}{month}{day}.mp3'.format(
            year=date.year,
            month='%02d'%(date.month,),
            day='%02d'%(date.day,),
            )

def _download_file(url, filename):
    print('-->downloading {}'.format(filename))
    urllib.urlretrieve(url, filename)

if __name__ == '__main__':
    print('start downloading...')
    while cur_date.year == 2007:
        url = _construct_url(cur_date)
        filename = '{}_{}_{}.mp3'.format(cur_date.year, cur_date.month, cur_date.day)
        _download_file(url, filename)
        cur_date += step
