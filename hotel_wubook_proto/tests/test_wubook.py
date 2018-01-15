# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Solucións Aloxa S.L. <info@aloxa.eu>
#                       Alexandre Díaz <dev@redneboa.es>
#
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
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT)
from openerp.exceptions import ValidationError
from .common import TestHotelWubook
from odoo.addons.hotel import date_utils
import pytz
import logging
_logger = logging.getLogger(__name__)


class TestWubook(TestHotelWubook):

    def test_create_reservation(self):
        now_utc_dt = date_utils.now()
        checkin_utc_dt = now_utc_dt + timedelta(days=3)
        checkin_dt = date_utils.dt_as_timezone(checkin_utc_dt,
                                               self.tz_hotel)
        checkout_utc_dt = checkin_utc_dt + timedelta(days=2)
        date_diff = date_utils.date_diff(checkin_utc_dt, checkout_utc_dt,
                                         hours=False) + 1

        wbooks = [self.create_wubook_booking(
            self.user_hotel_manager,
            checkin_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            self.partner_2,
            {
                self.hotel_vroom_budget.wrid: {
                    'occupancy': [1],   # 1 Reservation Line
                    'dayprices': [15.0, 15.0]   # 2 Days
                }
            }
        )]
        processed_rids, errors, checkin_utc_dt, checkout_utc_dt = \
            self.env['wubook'].generate_reservations(wbooks)

        # Check Creation
        self.assertTrue(any(processed_rids), "Reservation not found")
        nreserv = self.env['hotel.reservation'].search([
            ('wrid', '=', processed_rids[0])
        ], limit=0)
        self.assertTrue(nreserv, "Reservation not found")
        nfolio = self.env['hotel.folio'].search([
            ('id', '=', nreserv.folio_id.id)
        ], limit=1)
        self.assertTrue(nfolio, "Folio not found")

        # Check Dates
        self.assertEqual(
            nreserv.checkin,
            checkin_utc_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "Invalid Checkin Reservation Date")
        self.assertEqual(
            nreserv.checkout,
            checkout_utc_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            "Invalid Checkout Reservation Date")
        # Check Price
        self.assertEqual(nreserv.price_unit, 30.0, "Invalid Reservation Price")
        # Check Reservation Lines
        self.assertTrue(any(nreserv.reservation_lines),
                        "Reservation lines snot found")
        dates_arr = date_utils.generate_dates_list(checkin_dt, date_diff-1)
        for k_line, v_line in enumerate(nreserv.reservation_lines):
            self.assertEqual(dates_arr[k_line], v_line['date'],
                             "Invalid Reservation Lines Dates")
