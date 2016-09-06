# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class MedicalPharmacyLicense(models.Model):
    _name = 'medical.pharmacy.license'
    _description = 'Medical Pharmacy License'

    pharmacy_id = fields.Many2one(
        string='Pharmacy',
        comodel_name='medical.pharmacy',
        required=True,
        ondelete='restrict',
    )
    country_id = fields.Many2one(
        string='Country',
        comodel_name='res.country',
        required=True,
    )
    state_id = fields.Many2one(
        string='State',
        comodel_name='res.country.state',
        domain="[('country_id', '=', country_id)]",
    )
    license_num = fields.Char(
        required=True,
    )
    date_start = fields.Datetime(
        string='License Start',
        help='Date that this license begins',
    )
    date_end = fields.Datetime(
        string='License Expire',
        help='Date that this license is expired',
    )
