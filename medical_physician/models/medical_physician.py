# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Ken Mak <kmak@laslabs.com>
#    Copyright: 2014-2016 LasLabs, Inc. [https://laslabs.com]
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


class MedicalPhysician(models.Model):
    _name = 'medical.physician'
    _inherits = {'res.partner': 'partner_id', }
    _description = 'Medical Physicians'
    id = fields.Integer('ID', readonly=True)
    partner_id = fields.Many2one(
        'res.partner', 'Related Partner', required=True, ondelete='cascade',
        help='Partner related data of the physician'
    )
    code = fields.Char(size=256, string='ID')
    specialty_id = fields.Many2one(
        'medical.specialty', string='Specialty',
        default=lambda self: self.env['medical.specialty'].search([('name', '=', 'General Practitioner')]).id,
        required=True, help='Specialty Code'
    )
    info = fields.Text(string='Extra info')
    active = fields.Boolean(
        'Active', default=True,
        help='If unchecked, it will allow you to hide the physician without '
             'removing it.'
    )
    schedule_template_ids = fields.One2many(
        'medical.physician.schedule.template', 'physician_id',
        'Related schedules', help='Schedule template of the physician'
    )

    _defaults = {'is_doctor': True, 'supplier': True, 'active': True}

    @api.model
    def create(self, vals,):
        groups_proxy = self.env['res.groups']
        group_ids = groups_proxy.search([('name', '=', 'Medical Doctor')])
        vals['groups_id'] = [(6, 0, group_ids)]
        return super(MedicalPhysician, self).create(vals)
