# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
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

from openerp import fields, models
from openerp.addons.medical.medical_constants import days, hours, minutes

import logging

_logger = logging.getLogger(__name__)


class MedicalPhysicianScheduleTemplate(models.Model):
    '''
    Available schedule for the Physiscian.

    ie: A physiscian will be able to say, in this schedule on this days.

    The objective is to show the availbles spaces for every physiscian
    '''
    _name = 'medical.physician.schedule.template'
    physician_id = fields.Many2one(
        'medical.physician', 'Physician', required=True, select=1,
        ondelete='cascade'
    )
    day = fields.Selection(days, string='Day', sort=False)
    start_hour = fields.Selection(hours, string='Hour')
    start_minute = fields.Selection(minutes, string='Minute')
    end_hour = fields.Selection(hours, string='Hour')
    end_minute = fields.Selection(minutes, string='Minute')
    duration = fields.Selection(minutes, string='Duration')
