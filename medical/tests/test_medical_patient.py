# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of medical, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     medical is free software:
#     you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     medical is distributed in the hope that it will
#     be useful but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with medical.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from dateutil.relativedelta import relativedelta

from openerp import fields
from openerp.tests.common import TransactionCase
from datetime import date


class TestMedicalPatient(TransactionCase):

    def setUp(self):
        super(TestMedicalPatient, self).setUp()
        self.vals = {
            'name': 'Patient 1',
            'gender': 'm',
        }

    def test_sequence(self):
        patient_id = self.env['medical.patient'].create(self.vals)
        self.assertTrue(
            patient_id.identification_code, 'Should have a sequence')

    def test_age_computation(self):
        """
        Check value of age depending of the birth_date
        """
        age = 10
        complete_age = '10y 0m 0d'
        birth_date = fields.Date.to_string(
            date.today() - relativedelta(years=age)
        )
        self.vals['dob'] = birth_date
        patient_id = self.env['medical.patient'].create(self.vals)
        self.assertEquals(
            patient_id.age, complete_age,
            'Should be the same age.\rGot: %s\rExpected: %s' % (
                patient_id.age, complete_age
            )
        )

    def test_age_computation_deceased(self, ):
        """ Check proper handling of deceased patient """
        age = 5
        birth_date = fields.Date.to_string(
            date.today() - relativedelta(years=age*2)
        )
        self.vals.update({
            'dob': birth_date,
            'deceased': True,
            'dod': fields.Date.to_string(
                date.today() - relativedelta(years=age)
            )
        })
        patient_id = self.env['medical.patient'].create(self.vals)
        dod_age = '5y 0m 0d'
        expect = '%s (deceased)' % dod_age
        self.assertEquals(
            patient_id.age, expect,
            'Did not properly handle deceased.\rGot: %s\rExpected: %s' % (
                patient_id.age, expect
            )
        )

    def test_invalidate(self):
        """
        Invalidate a patient should invalidate its diseases
        """
        patient_id = self.env['medical.patient'].create(self.vals)
        self.assertTrue(patient_id.active, 'Should be active')
        self.assertTrue(patient_id.partner_id.active, 'Should be inactive')
        self.assertFalse(patient_id.dod, 'Should be empty')
        patient_id.action_invalidate()
        self.assertFalse(patient_id.active, 'Should be inactive')
        self.assertFalse(patient_id.partner_id.active, 'Should be inactive')
