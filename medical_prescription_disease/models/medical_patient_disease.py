# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class MedicalPatientDisease(models.Model):
    _inherit = 'medical.patient.disease'
    prescription_order_line_ids = fields.One2many(
        string='Prescription Lines',
        comodel_name='medical.prescription.order.line',
        inverse_name='disease_id',
        help='Prescriptions related to this disease.',
    )
    count_prescription_order_line_ids = fields.Integer(
        compute='_compute_prescription_order_lines',
        string='Prescription Order Lines',
    )
    last_prescription_order_line_date = fields.Datetime(
        compute='_compute_prescription_order_lines',
        string='Last Prescription Order Line',
    )
    last_prescription_order_line_state = fields.Selection(
        [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        compute='_compute_prescription_order_lines',
        default='active',
        string='Last Prescription Order Line',
    )

    @api.multi
    def _compute_prescription_order_lines(self, ):
        for rec_id in self:
            line_ids = rec_id.prescription_order_line_ids

            if line_ids:
                rec_id.count_prescription_order_line_ids = len(line_ids)

                sorted_line_ids = line_ids.sorted(
                    key=lambda r: r.date_start_treatment,
                    reverse=True,
                )
                last_line_id = sorted_line_ids[0]
                last_line_date = last_line_id.date_start_treatment

                rec_id.last_prescription_order_line_date = last_line_date

                if last_line_id.is_course_complete:
                    rec_id.last_prescription_order_line_state = 'inactive'
                else:
                    rec_id.last_prescription_order_line_state = 'active'
