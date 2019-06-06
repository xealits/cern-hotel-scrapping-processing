from pathlib import Path
from datetime import datetime
import csv
import sys, os
import numpy
import pickle
import logging


logging.basicConfig(level=logging.INFO)

data_dir = Path('../data') #.exists()

logging.info("gathering data from the directory %s" % data_dir)

data = {}
'''
data = {record_tuple (Y, M, WEEK, WD, H):
{(year, month, week, day): load}

old:
data = {record_tuple (Y, M, D, H):
{(year, month, week, day): load}
'''

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
    'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12}

availabilities = {'': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4, 'closed': 5}

logging.info("turning off the stdout")

sys_stdout = sys.stdout
devnull = open(os.devnull, 'w')
sys.stdout = devnull

for record in data_dir.iterdir():
    day, hour = record.name.split('_') # had to use the same delimiter everywhere
    h = int(hour) // 6 # quarters of a day
    y, m, d = [int(i) for i in day.split('-')]
    date = datetime.strptime(day, '%Y-%m-%d') # YYYY-0M-0D
    wd = int(date.weekday()) # in datetime weekdays start from 0 and end at 6 -- same as in scrap data
    week_n = (d - wd) // 7 + (((d - wd) % 7) > 0) # the week of the month
    #record_tuple = tuple(y, m, d, h) # old tuple with month-days
    record_tuple = (y, m, week_n, wd, h)
    record_data = dict()
    data[record_tuple] = record_data
    #if x.is_dir()]
    for month_data_file in record.iterdir():
        month, year = month_data_file.name.split('_')
        m = months[month]
        y = int(year)
        with month_data_file.open() as f:
            r = csv.reader(f)
            next(r), next(r) # skip header lines # <--------- this prints to console!
            #sys.stdout = sys.__stdout__ # doesn't work
            for wday, day, avail in r:
                wd = int(wday[2:])
                d  = int(day[1:])
                # the week of the day = full weeks + starting part-week
                week_n = (d - wd) // 7 + (((d - wd) % 7) > 0)
                # each row = [wdN, dN, avail]
                # wdN = 'wdN' -- int starts from position 2
                #print(row)
                if avail not in availabilities:
                    sys.stdout = sys_stdout
                    print(record_tuple, y, m, wd, avail)
                    sys.stdout = devnull
                    continue
                record_data[(y, m, week_n, wd)] = availabilities[avail]
                if wd == 'wd6': week_n += 1

sys.stdout = sys_stdout

logging.info("done, dumping pickle")

pickle.dump(data, open('data2.p', 'wb')) #, protocol=2)

