# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class MedicalMedicamentComponent(models.Model):
    _name = 'medical.medicament.component'
    _description = 'Medical Medicament Component'

    medicament_ids = fields.Many2many(
        string='Related Medicaments',
        comodel_name='medical.medicament',
    )
    name = fields.Char(
        help='Component name.',
    )
    is_active_ingredient = fields.Boolean(
        string='Active Ingredient?',
        help='Check this if the component is an active ingredient.',
    )
