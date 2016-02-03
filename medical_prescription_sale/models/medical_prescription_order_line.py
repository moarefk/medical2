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

from openerp import fields, models, api


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    sale_order_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='prescription_order_line_id',
        readonly=True,
    )
    sale_order_ids = fields.Many2many(
        comodel_name='sale.order',
        compute='_compute_dispensings_and_orders',
        readonly=True,
    )
    dispensed_ids = fields.One2many(
        'procurement.order',
        compute='_compute_dispensings_and_orders',
        readonly=True,
    )
    dispensed_qty = fields.Float(
        default=0.0,
        readonly=True,
        compute='_compute_dispensings_and_orders',
        help='Amount already dispensed (using medicine dosage)',
    )
    pending_dispense_qty = fields.Float(
        default=0.0,
        readounly=True,
        compute='_compute_dispensings_and_orders',
        help='Amount pending dispense (using medicine dosage)',
    )
    exception_dispense_qty = fields.Float(
        default=0.0,
        readounly=True,
        compute='_compute_dispensings_and_orders',
        help='Qty of dispense exceptions (using medicine dosage)',
    )
    cancelled_dispense_qty = fields.Float(
        default=0.0,
        readounly=True,
        compute='_compute_dispensings_and_orders',
        help='Dispense qty cancelled (using medicine dosage)',
    )
    can_dispense = fields.Boolean(
        compute='_compute_can_dispense_and_qty',
        default=False,
        readonly=True,
        help='Can this prescription be dispensed?',
    )
    can_dispense_qty = fields.Float(
        compute='_compute_can_dispense_and_qty',
        default=0.0,
        help='Amount that can be dispensed (using medicine dosage)',
    )
    name = fields.Char(
        default=lambda s: s._default_name(),
        required=True,
    )
    receive_method = fields.Selection([
        ('online', 'E-Prescription'),
        ('phone', 'Phoned In'),
        ('fax', 'Fax'),
        ('mail', 'Physical Mail'),
        ('transfer', 'Transferred In'),
    ],
        default='fax',
        string='Receipt Method',
        help='How the Rx was received',
    )
    verify_method = fields.Selection([
        ('none', 'Not Verified'),
        ('doctor_phone', 'Called Doctor'),
    ],
        default='none',
        help='Method of Rx verification',
    )
    receive_date = fields.Datetime(
        default=lambda s: fields.Datetime.now,
        string='Receipt Date',
        help='When the Rx was received',
    )

    @api.multi
    def _compute_dispensings_and_orders(self, ):
        ''' Get related dispensings and orders. Also sets dispense qty's '''

        for rec_id in self:
    
            dispense_ids = self.env['procurement.order']
            order_ids = self.env['sale.order']
            dispense_qty = 0.0
            pending_qty = 0.0
            cancel_qty = 0.0
            except_qty = 0.0

            for line_id in rec_id.sale_order_line_ids:
    
                order_ids += line_id.order_id
                for proc_id in line_id.procurement_ids:
    
                    dispense_ids += proc_id.id
    
                    if proc_id.product_uom.id != rec_id.dispense_uom_id.id:
                        _qty = proc_id.product_uom._compute_qty_obj(
                            proc_id.product_qty, rec_id.dispense_uom_id
                        )
                    else:
                        _qty = rec_id.dispense_uom_id
    
                    if proc_id.state == 'done':
                        dispense_qty += _qty
                    elif proc_id.state in ['confirmed', 'running']:
                        pending_qty += _qty
                    elif proc_id.state == 'cancel':
                        cancel_qty += _qty
                    else:
                        except_qty += _qty

            rec_id.cancelled_dispense_qty = cancel_qty
            rec_id.dispensed_qty = dispense_qty
            rec_id.pending_dispense_qty = pending_qty
            rec_id.exception_dispense_qty = except_qty
            rec_id.order_ids = set(order_ids)
            rec_id.dispensed_ids = set(dispense_ids)

    @api.multi
    def _compute_can_dispense_and_qty(self, ):
        '''
        Determine whether Rx can be dispensed based on current dispensings,
        and what qty
        '''

        for rec_id in self:

            total = sum(rec_id.dispensed_qty, rec_id.exception_dispense_qty,
                        rec_id.pending_dispense_qty)

            if rec_id.qty > total:
                rec_id.can_dispense = True
                rec_id.can_dispense_qty = self.qty - total
            else:
                rec_id.can_dispense = False
                rec_id.can_dispense_qty = self.qty - total

    @api.model
    def _default_name(self, ):
        return self.env['ir.sequence'].get('medical.prescription.order.line')
