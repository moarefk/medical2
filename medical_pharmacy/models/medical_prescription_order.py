# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2015 LasLabs, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models


class MedicalPrescriptionOrder(models.Model):
    _inherit = 'medical.prescription.order'

    state = field.Selection(
        [
            ('draft', 'Draft'),
            ('progress', 'Open'),
            ('matched', 'Matched Sale'),
            ('manual', 'To Invoice'),
            ('dispense', 'To Dispense'),
            ('dispense_except', 'Dispense Exception'),
            ('verify_except', 'Verification Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('cancel', 'Canceled'),
            ('dispensed', 'Dispensed'),
        ],
        default = 'draft',
        readonly = True,
        string = 'Rx State',
        help = 'Current workflow status of Rx',
    )
    receive_method = fields.Selection(
        [
            ('phone', 'Phoned In'),
            ('fax', 'Physical Fax'),
            ('mail', 'Physical Mail'),
            ('transfer', 'Transferred In'),
        ],
        default = 'phone',
        string = 'Receipt Method',
        help = 'How the Rx was received',
    )
    verify_method = fields.Selection(
        [
            ('doctor_phone', 'Called Doctor')
        ]
    )
    receive_date = fields.Datetime(
        default = fields.Datetime.now,
        string = 'Receipt Date',
        help = 'When the Rx was received',
    )
    image = fields.Binary(
        help = 'PNG representation of Rx',
    )
    
