#!/usr/local/bin/python

import argparse
import urllib
from datetime import date, timedelta

_DATE_SEPARATOR = '-'
#TODO: use Enum instead
_MONDAY = 'Monday'
_TUESDAY = 'Tuesday'
_WEDNESDAY = 'Wednesday'
_THURSDAY = 'Tuesday'
_FRIDAY = 'Friday'


def _construct_url(date):
    return 'http://swtychina.com/gb/audiodoc/{year}/{year}{month}/{year}{month}{day}.mp3'.format(
            year=date.year,
            month='%02d'%(date.month,),
            day='%02d'%(date.day,),
            )

def _download_file(url, filename):
    print('-->downloading {}'.format(filename))
    urllib.urlretrieve(url, filename)

def _parse_string_to_date(date_str):
    #TODO: add more checking about date_str format
    date_list = date_str.split(_DATE_SEPARATOR)
    date_list = map(int, date_list)
    return date(*date_list)

def _download_program_of_date(date):
    url = _construct_url(date)
    filename = '{}_{}_{}.mp3'.format(cur_date.year, cur_date.month, cur_date.day)
    _download_file(url, filename)

def _start_download(start_date, end_date, chosen_weekdays):
    #TODO
    pass

def _extract_chosen_weekdays_from_args(args):
    if args.all_weekday:
        return [_MONDAY, _TUESDAY, _WEDNESDAY, _THURSDAY, _FRIDAY]
    else:
        #TODO: prettify this
        chosen_weekdays = []
        if args.mon:
            chosen_weekdays += [_MONDAY]
        if args.tue:
            chosen_weekdays += [_TUESDAY]
        if args.wed:
            chosen_weekdays += [_WEDNESDAY]
        if args.thu:
            chosen_weekdays += [_THURSDAY]
        if args.fri:
            chosen_weekdays += [_FRIDAY]
        return chosen_weekdays

def main():
    parser = argparse.ArgumentParser('swty downloader')
    parser.add_argument('start_date', type=str, help='start date of downloading')
    parser.add_argument('end_date', type=str, help='end date of downloading')
    parser.add_argument('--mon', action='store_true', help='download Monday program')
    parser.add_argument('--tue', action='store_true', help='download Tuesday program')
    parser.add_argument('--wed', action='store_true', help='download Wednesday program')
    parser.add_argument('--thu', action='store_true', help='download Thursday program')
    parser.add_argument('--fri', action='store_true', help='download Friday program')
    args = parser.parse_args()

    if not any((args.mon, args.tue, args.wed, args.thu, args.fri)):
        args.all_weekday = True
    else:
        args.all_weekday = False

    start_date = _parse_string_to_date(args.start_date)
    end_date = _parse_string_to_date(args.end_date)

    chosen_weekdays = _extract_chosen_weekdays_from_args(args)

    print('Downloading swty *{}* programs from {} to {}...'.format(
        ' '.join(chosen_weekdays),
        start_date,
        end_date
        )
    )

    _start_download(start_date, end_date, chosen_weekdays)

if __name__ == '__main__':
    main()
