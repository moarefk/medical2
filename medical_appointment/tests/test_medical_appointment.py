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

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from datetime import datetime


class TestMedicalAppointment(TransactionCase):

    def setUp(self, ):
        super(TestMedicalAppointment, self).setUp()
        vals = {
            'name': 'Test Patient',
        }
        patient_id = self.env['medical.patient'].create(vals)
        vals = {
            'name': 'Test Specialty',
            'code': 'TS',
        }
        specialty_id = self.env['medical.specialty'].create(vals)
        vals = {
            'name': 'Test Physician',
            'specialty_id': specialty_id.id,
        }
        self.physician_id = self.env['medical.physician'].create(vals)
        vals = {
            'name': 'default',
            'is_default': True,
        }
        self.env['medical.appointment.stage'].write(vals)
        vals = {
            'name': 'review',
            'is_default': False,
        }
        self.env['medical.appointment.stage'].write(vals)
        vals = {
            'name': 'cancelled',
            'is_default': False,
        }
        self.env['medical.appointment.stage'].write(vals)
        vals = {
            'name': 'Test Appointment 1',
            'patient_id': patient_id.id,
            'physician_id': self.physician_id.id,
            'appointment_type': 'outpatient',
            'appointment_date': datetime(2016, 1, 1, 11, 0, 0),
            'duration': 60,
        }
        self.appointment_id = self.env['medical.appointment'].create(vals)
        vals = {
            'name': 'Test Appointment 2',
            'patient_id': patient_id.id,
            'physician_id': self.physician_id.id,
            'appointment_type': 'outpatient',
            'appointment_date': datetime(2016, 1, 1, 11, 30, 0),
            'duration': 60,
        }
        self.appointment_id2 = self.env['medical.appointment'].create(vals)
        vals = {
            'name': 'Test Appointment 3',
            'patient_id': patient_id.id,
            'physician_id': self.physician_id.id,
            'appointment_type': 'outpatient',
            'appointment_date': datetime(2016, 1, 1, 15, 0, 0),
            'duration': 60,
        }
        self.appointment_id3 = self.env['medical.appointment'].create(vals)
        vals = {
            'name': 'Test Institution',
            'is_institution': True,
        }
        self.institution_id = self.env['res.partner'].create(vals)

    def test_default_stage_id(self, ):
        default_stage = self.appointment_id._default_stage_id()
        self.assertEqual('default', default_stage.name)

    def test_group_stage_ids(self, ):
        expect = ['default', 'review', 'cancelled', ]
        got = self.appointment_id._group_stage_ids()
        self.assertEquals(expect, got[0])

    def test_get_appointments(self, ):
        vals = {
            'module': 'medical_appointment',
            'id': 'stage_appointment_cancelled',
            'name': 'cancelled'
        }
        self.env['ir.model.data'].write(vals)
        vals = {
            'module': 'medical_appointment',
            'id': 'stage_appointment_in_review',
            'name': 'review',
        }
        self.env['ir.model.data'].write(vals)
        got = self.appointment_id._get_appointments(
            self.physician_id,
            self.institution_id,
            datetime(2016, 1, 1, 11, 0, 0),
            datetime(2016, 1, 1, 12, 0, 0),
        )
        self.assertEqual(2, got.count())

    def test_clashes_state_to_review_error(self, ):
        with self.assertRaises(ValueError):
            self.appointment_id._set_clashes_state_to_review(
                self.physician_id,
                self.institution_id,
                datetime(2016, 1, 1, 14, 0, 0),
                datetime(2016, 1, 1, 16, 0, 0),
            )

    def test_clashes_state_to_review_no_error(self, ):
        vals = {
            'module': 'medical_appointment',
            'id': 'stage_appointment_in_review',
            'name': 'review',
        }
        self.env['ir.model.data'].write(vals)
        self.appointment_id._set_clashes_state_to_review(
            self.physician_id,
            self.institution_id,
            datetime(2016, 1, 1, 12, 0, 0),
            datetime(2016, 1, 1, 12, 0, 0),
        )
        self.assertEquals('review', self.appointment_id.stage_id.name)

    def test_check_not_double_booking_booked(self, ):
        with self.assertRaises(ValidationError):
            self.appointment_id._check_not_double_booking()

    def test_check_not_double_booking_not_booked(self, ):
        with self.assertRaises(ValidationError):
            try:
                self.appointment_id3._check_not_double_booking()
            except:
                pass
            else:
                raise ValidationError
