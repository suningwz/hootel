# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 Solucións Aloxa S.L. <info@aloxa.eu>
#                       Alexandre Díaz <dev@redneboa.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime, timedelta
import pytz
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT)
from openerp import fields
from openerp.exceptions import ValidationError


# Generate a 'datetime' object from 'str_date' string with 'dtformat' format.
def _generate_datetime(str_date, dtformat, tz=False):
    ndate = False
    try:
        ndate = datetime.strptime(str_date, dtformat)
        ndate = ndate.replace(tzinfo=pytz.timezone(tz and str(tz) or 'UTC'))
    except ValueError:
        return False

    return ndate


# Try generate a 'datetime' object from 'str_date' string
# using all odoo formats
def get_datetime(str_date, hours=True, end_day=False, tz=False):
    date_dt = _generate_datetime(
        str_date,
        DEFAULT_SERVER_DATETIME_FORMAT,
        tz=tz)
    if not date_dt:
        date_dt = _generate_datetime(
            str_date,
            DEFAULT_SERVER_DATE_FORMAT,
            tz=tz)

    if date_dt:
        if end_day:
            date_dt = date_dt.replace(hour=23, minute=59, second=59,
                                      microsecond=999999)
        elif not hours:
            date_dt = date_dt.replace(hour=0, minute=0, second=0,
                                      microsecond=0)

    return date_dt


# Compare two dates
def date_compare(str_date_a, str_date_b, hours=True):
    date_dt_a = get_datetime(str_date_a)
    date_dt_b = get_datetime(str_date_b)

    if not hours:
        date_dt_a = date_dt_a.replace(hour=0, minute=0, second=0,
                                      microsecond=0)
        date_dt_b = date_dt_b.replace(hour=0, minute=0, second=0,
                                      microsecond=0)

    return date_dt_a == date_dt_b


# Get now 'datetime' object
def now(hours=False):
    now_utc_dt = fields.datetime.now().replace(tzinfo=pytz.utc)

    if not hours:
        now_utc_dt = now_utc_dt.replace(hour=0, minute=0, second=0,
                                        microsecond=0)

    return now_utc_dt


# Get the difference in days between 'str_date_start' and 'str_date_end'
def date_diff(date_start, date_end, hours=True, tz=False):
    if not isinstance(date_start, datetime):
        date_start_dt = get_datetime(date_start, tz=tz)
    else:
        date_start_dt = date_start
    if not isinstance(date_end, datetime):
        date_end_dt = get_datetime(date_end, tz=tz)
    else:
        date_end_dt = date_end

    if not date_start_dt or not date_end_dt:
        raise ValidationError("Invalid date. Can't compare it!")

    if not hours:
        date_start_dt = date_start_dt.replace(hour=0, minute=0, second=0,
                                              microsecond=0)
        date_end_dt = date_end_dt.replace(hour=0, minute=0, second=0,
                                          microsecond=0)

    return abs((date_end_dt - date_start_dt).days)


# Get a new 'datetime' object from 'date_dt' usign the 'tz' timezone
def dt_as_timezone(date_dt, tz):
    return date_dt.astimezone(pytz.timezone(tz and str(tz) or 'UTC'))


# Generate a tuple of days start in 'cdate'
def generate_dates_list(cdate,
                        num_days,
                        outformat=DEFAULT_SERVER_DATE_FORMAT, tz=False):
    ndate = get_datetime(cdate, tz=tz) if not isinstance(cdate, datetime) \
        else cdate
    return [(ndate + timedelta(days=i)).strftime(outformat)
            for i in range(0, num_days)]


# Check if 'str_date' is between 'str_start_date' and 'str_end_date'
#   0   Inside
#   -1  'str_date' is before 'str_start_date'
#   1   'str_date' is after 'str_end_date'
def date_in(str_date, str_start_date, str_end_date, hours=True, tz=False):
    date_dt = get_datetime(str_date, tz=tz)
    date_start_dt = get_datetime(str_date_start, tz=tz)
    date_end_dt = get_datetime(str_date_end, tz=tz)

    if not date_start_dt or not date_end_dt or not date_dt:
        raise ValidationError("Invalid date. Can't compare it!")

    if not hours:
        date_start_dt = date_start_dt.replace(hour=0, minute=0, second=0,
                                              microsecond=0)
        date_end_dt = date_end_dt.replace(hour=23, minute=59, second=59,
                                          microsecond=999999)

    res = -2
    if date_dt >= date_start_dt and date_dt <= date_end_dt:
        res = 0
    elif date_dt > date_end_dt:
        res = 1
    elif date_dt < date_start_dt:
        res = -1

    return res


# Check if 'str_start_date_a' and 'str_start_date_b'
# is between 'str_start_date_b' and 'str_end_date_b'
#   0   Inside
#   -1  'str_date' is before 'str_start_date'
#   1   'str_date' is after 'str_end_date'
def range_dates_in(str_start_date_a,
                   str_end_date_a,
                   str_start_date_b,
                   str_end_date_b,
                   hours=True, tz=False):
    date_start_dt_a = get_datetime(str_start_date_a, tz=tz)
    date_end_dt_a = get_datetime(str_end_date_a, tz=tz)
    date_start_dt_b = get_datetime(str_start_date_b, tz=tz)
    date_end_dt_b = get_datetime(str_end_date_b, tz=tz)

    if not date_start_dt_a or not date_end_dt_a \
            or not date_start_dt_b or not date_end_dt_b:
        raise ValidationError("Invalid date. Can't compare it!")

    if not hours:
        date_start_dt_b = date_start_dt_b.replace(hour=0, minute=0, second=0,
                                                  microsecond=0)
        date_end_dt_b = date_end_dt_b.replace(hour=23, minute=59, second=59,
                                              microsecond=999999)

    res = -2
    if date_start_dt_a >= date_start_dt_b and date_end_dt_a <= date_end_dt_b:
        res = 0
    elif date_start_dt_a < date_start_dt_b \
            and date_end_dt_a >= date_start_dt_b:
        res = -1
    elif date_start_dt_a <= date_end_dt_b and date_end_dt_a > date_end_dt_b:
        res = 1

    return res