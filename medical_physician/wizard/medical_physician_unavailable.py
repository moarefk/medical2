# -*- encoding: utf-8 -*-
###############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
# Copyright (C) 2008-2009 AJM Technologies S.A. (<http://www.ajm.lu). All
# Rights Reserved
# Copyright (C) 2010-2011 Thamini S.à.R.L (<http://www.thamini.com>). All
# Rights Reserved
# $Id$
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import fields, models


class medical_physician_unavailable_wizard(models.TransientModel):
    _name = 'medical.physician.unavailable.wizard'
    _description = 'Medical physicians unavailable wizard'
    physician_id = fields.Many2one(
        'medical.physician', 'Physician', required=True
        )
    date_start = fields.Datetime(
        string='Start', default=fields.date.today, required=True
        )
    date_end = fields.Datetime(
        string='End', default=fields.date.today, required=True
        )
    institution_id = fields.Many2one(
        'res.partner', 'Medical Center', select=True,
        domain=[('is_institution', '=', True)]
        )

    def action_cancel(self, cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}

    def action_set_unavailable(self, cr, uid, ids, context=None):
        if not ids:
            return {}

        appointment_proxy = self.pool['medical.appointment']

        this = self.browse(cr, uid, ids)[0]
        physician_id = this.physician_id.id
        institution_id = this.institution_id.id
        if institution_id:
            institution_ids = [institution_id]
        else:
            institution_ids = []

        date_start = this.date_start
        date_end = this.date_end

        appointment_proxy._remove_empty_clashes(cr, uid, [], [physician_id],
                                                institution_ids, date_start,
                                                date_end, context=context)
        appointment_proxy._set_clashes_state_to_review(cr, uid, [physician_id],
                                                       institution_ids,
                                                       date_start, date_end,
                                                       context=context)

        return {'type': 'ir.actions.act_window_close'}
