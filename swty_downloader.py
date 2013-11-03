#!/usr/local/bin/python

import argparse
import os
import urllib
from datetime import date, timedelta

_DATE_SEPARATOR = '-'
#TODO: use Enum instead
_MONDAY = 'Monday'
_TUESDAY = 'Tuesday'
_WEDNESDAY = 'Wednesday'
_THURSDAY = 'THURSDAY'
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

def _download_program_of_date(date, subfolder):
    url = _construct_url(date)
    filename = '{}_{}_{}.mp3'.format(date.year, date.month, date.day)
    #TODO: need to fix this ugliness
    try:
        os.mkdir(subfolder)
    except OSError:
        pass
    #TODO use os.path instead
    _download_file(url, subfolder + '/' + filename)

def _download_certain_weekday_program(start_date, end_date, day):
    #TODO use a more pythonic way
    print('==>')
    cur_date = start_date
    while cur_date <= end_date:
        if cur_date.weekday() == day:
            #TODO: use weekday name as subfolder name
            _download_program_of_date(cur_date, str(day))
            cur_date += timedelta(days=7)
        else:
            cur_date += timedelta(days=1)

def _start_download(start_date, end_date, chosen_weekdays):
    for day in chosen_weekdays:
        _download_certain_weekday_program(start_date, end_date, day)

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

def _transform_weekday_to_int(day):
    if day == _MONDAY:
        return 0
    elif day == _TUESDAY:
        return 1
    elif day == _WEDNESDAY:
        return 2
    elif day == _THURSDAY:
        return 3
    elif day == _FRIDAY:
        return 4

def _parse_chosen_weekdays_to_standard_rep(chosen_weekdays):
    return map(_transform_weekday_to_int, chosen_weekdays)

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

    chosen_weekdays_standard_rep = _parse_chosen_weekdays_to_standard_rep(chosen_weekdays)

    _start_download(start_date, end_date, chosen_weekdays_standard_rep)

if __name__ == '__main__':
    main()
