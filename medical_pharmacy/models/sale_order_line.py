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

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _compute_dispense_qty(self, ):
        return True
        rx_line = self.prescription_order_line_id
        if self.product_uom == rx_line.dispense_uom_id:
            self.dispense_qty = self.product_uom_qty
        else:
            self.dispense_qty = proc_id.product_uom._compute_qty_obj(
                self.product_uom_qty, rx_line.dispense_uom_id
            )

    patient_id = fields.Many2one(
        string='Patient',
        comodel_name='medical.patient',
        related='prescription_order_line_id.patient_id',
    )
    prescription_order_line_id = fields.Many2one(
        string='Prescription Line',
        comodel_name='medical.prescription.order.line',
    )
    medication_id = fields.Many2one(
        string='Medication',
        comodel_name='medical.patient.medication',
        related='prescription_order_line_id.medical_medication_id',
    )
    dispense_qty = fields.Float(
        default=0.0,
        readonly=True,
        compute='_compute_dispense_qty',
    )
    state = fields.Selection(selection_add=[
        ('rx_verify', 'Rx Verification'),
    ])
    #
    # @api.one
    # @api.constrains(
    #     'product_id', 'prescription_order_line_id', 'patient_id',
    # )
    # def _check_sale_line_prescription(self, ):
    #     '''
    #     Validate whether the line can be dispensed based on Rx, pending
    #     dispensings, etc.
    #     :returns: bool -- If line can be processed
    #     :raises: :class:`openerp.exceptions.ValidationError`
    #     '''
    #
    #     if not self.medication_id.medicament_id.is_medicament:
    #         return True
    #     if not self.medication_id.medicament_id.is_prescription:
    #         return True
    #
    #     rx_line = self.prescription_order_line_id
    #
    #     if self.patient_id != rx_line.patient_id:
    #         raise ValidationError(_(
    #             'Patients must be same on Order and Rx lines. '
    #             'Got %s on order line %d, expected %s from rx line %d' % (
    #                 self.patient_id.name, self.id,
    #                 rx_line.patient_id.name, rx_line.id,
    #             ),
    #         ))
    #
    #     if rx_line.product_id != self.product_id:
    #         if not self.is_substitutable:
    #             raise ValidationError(_(
    #                 'Products must be same on Order and Rx lines. '
    #                 'Got %s on order line %d, expected %s from rx line %d' % (
    #                     self.product_id.name, self.id,
    #                     rx_line.product_id.name, rx_line.id,
    #                 ),
    #             ))
    #         else:
    #             raise NotImplementedError(_(
    #                 'Drug substitution validation has not been implemented.'
    #             ))
    #
    #     if not rx_line.can_dispense:
    #         raise ValidationError(_(
    #             'Cannot dispense - currently %f pending and %f exception.' % (
    #                 rx_line.pending_dispense_qty,
    #                 rx_line.exception_dispense_qty,
    #             )
    #         ))
    #
    #     if self.dispense_qty > rx_line.can_dispense_qty:
    #         raise ValidationError(_(
    #             'Cannot dispense - Order line %s goes over Rx qty by %d' % (
    #                 self.name, self.dispense_qty - rx_line.can_dispense_qty
    #             )
    #         ))
    #
    #     return True
