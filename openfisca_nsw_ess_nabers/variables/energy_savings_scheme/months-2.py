import calendar
from datetime import datetime

""" 
Finds the calendar date corresponding to the day of the 
month in the following month.

For example, if give 15-01-2020 it should return
15-02-2020.

If the following month does not have that day, it 
returns the first day of the month after. For example
if given 30-01-2020, it should return 1-03-2020, as there
is no such thing as the 30th of Feb.

Returns a datetime object 
"""


def find_corresponding_date(start_date):
    day = start_date.day
    month = start_date.month
    year = start_date.year
    next_month = month + 1
    next_year = year

    if month == 12:
        next_month = 1
        next_year = year+1

    cal = calendar.Calendar()

    for cur_date in cal.itermonthdays3(next_year, next_month):
        (y, m, d) = cur_date
        print(cur_date)
        if m < next_month:
            continue
        if m > next_month:
            return datetime(year=cur_date[0], month=cur_date[1], day=cur_date[2])
        if d < day:
            continue
        if d == day:
            return datetime(year=cur_date[0], month=cur_date[1], day=cur_date[2])


def find_corresponding_date2(start_date):
    day = start_date.day
    month = start_date.month
    year = start_date.year
    next_month = month + 1
    next_year = year

    if month == 12:
        next_month = 1
        next_year = year+1

    try:
        new_date = datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year+1
        new_date = datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date

if __name__ == "__main__":
    start_date = datetime(day=30, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)
    print()

    start_date = datetime(day=15, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)
    print()
 
    start_date = datetime(day=31, month=12, year=2020)
    corres_date = find_corresponding_date(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=31, month=12, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=10, month=12, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=28, month=1, year=2019)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=29, month=1, year=2019)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=29, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=30, month=1, year=2019)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=30, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=30, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=30, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=15, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=31, month=7, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=31, month=8, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=10, month=5, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=4, month=3, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=1, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=1, month=1, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=1, month=12, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()

    start_date = datetime(day=31, month=12, year=2020)
    corres_date = find_corresponding_date2(start_date)
    print(start_date)
    print(corres_date)   
    print()
