#!/usr/local/bin/python

import argparse
import datetime
import os
import urllib


_DATE_SEPARATOR = '-'

class Weekday:
  MONDAY = 0
  TUESDAY = 1
  WEDNESDAY = 2
  THURSDAY = 3
  FRIDAY = 4
  SATURDAY = 5
  SUNDAY = 6
  WORKDAYS = [
      MONDAY,
      TUESDAY,
      WEDNESDAY,
      THURSDAY,
      FRIDAY
      ]
  WEEKENDS = [
      SATURDAY,
      SUNDAY,
      ]
  WEEKDAYS = WORKDAYS + WEEKENDS


_MAP_WEEKDAY_TO_STR = {
      Weekday.MONDAY: 'Monday',
      Weekday.TUESDAY: 'Tuesday',
      Weekday.WEDNESDAY: 'Wednesday',
      Weekday.THURSDAY: 'Thursday',
      Weekday.FRIDAY: 'Friday',
      Weekday.SATURDAY: 'Saturday',
      Weekday.SUNDAY: 'Sunday',
    }


def _construct_url(date):
    return 'http://swtychina.com/gb/audiodoc/{year}/{year}{month:02d}/{year}{month:02d}{day:02d}.mp3'.format(
            year=date.year,
            month=date.month,
            day=date.day,
            )

def _download_file(url, filename):
    print('-->downloading {}'.format(filename))
    urllib.urlretrieve(url, filename)

def _parse_string_to_date(date_str):
    #TODO: add more checking about date_str format
    date_list = date_str.split(_DATE_SEPARATOR)
    date_list = map(int, date_list)
    return datetime.date(*date_list)

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
    weekday_name = _MAP_WEEKDAY_TO_STR[day]
    print('==>downloading {} programs'.format(weekday_name))
    cur_date = start_date
    while cur_date <= end_date:
        if cur_date.weekday() == day:
            _download_program_of_date(cur_date, weekday_name)
            cur_date += datetime.timedelta(days=7)
        else:
            cur_date += datetime.timedelta(days=1)

def _start_download(start_date, end_date, chosen_weekdays):
    for day in chosen_weekdays:
        _download_certain_weekday_program(start_date, end_date, day)

def _extract_chosen_workdays_from_args(args):
    chosen_workdays = []
    if args.mon:
        chosen_workdays.append(Weekday.MONDAY)
    if args.tue:
        chosen_workdays.append(Weekday.TUESDAY) 
    if args.wed:
        chosen_workdays.append(Weekday.WEDNESDAY)
    if args.thu:
        chosen_workdays.append(Weekday.THURSDAY)
    if args.fri:
        chosen_workdays.append(Weekday.FRIDAY) 

    if len(chosen_workdays) == 0:
      # if none of the workdays is chosen then return all workdays
      return Weekday.WORKDAYS
    else:
      return chosen_workdays

def _print_download_title(start_date, end_date, chosen_workdays):
    print('Downloading swty *{}* programs from {} to {}...'.format(
        ' '.join(map(lambda wd:_MAP_WEEKDAY_TO_STR[wd] ,chosen_workdays)),
        start_date,
        end_date
        )
    )

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

    start_date = _parse_string_to_date(args.start_date)
    end_date = _parse_string_to_date(args.end_date)
    chosen_workdays = _extract_chosen_workdays_from_args(args)
    _print_download_title(start_date, end_date, chosen_workdays)

    _start_download(start_date, end_date, chosen_workdays)

if __name__ == '__main__':
    main()
