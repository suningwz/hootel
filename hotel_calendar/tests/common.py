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
from odoo.addons.hotel.tests.common import TestHotel


class TestHotelCalendar(TestHotel):

    @classmethod
    def setUpClass(cls):
        super(TestHotelCalendar, cls).setUpClass()

        # Minimal Hotel Calendar Configuration
        cls.tz_hotel = 'Europe/Madrid'
        cls.parity_pricelist_id = cls.pricelist_1.id
        cls.parity_restrictions_id = cls.restriction_1.id
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'divide_rooms_by_capacity',
                                                True)
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'type_move', 'normal')
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'end_day_week', 6)
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'default_num_days', 'month')
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'default_arrival_hour',
                                                '14:00')
        cls.env['ir.values'].sudo().set_default('hotel.config.settings',
                                                'default_departure_hour',
                                                '12:00')
