# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.exceptions import ValidationError


class MedicalAbstractLuhn(models.AbstractModel):
    """ Inherit this to provide Luhn validation to any model.

    Public attributes and methods will be prefixed with luhn in order
    to avoid name collisions with models that will inherit from this class.
    """

    _name = 'medical.abstract.luhn'

    @api.model
    def _luhn_is_valid(self, num):
        """ Determine whether num is valid. Meant to be used in constrains
        Params:
            num: ``str`` or ``int`` Number to validate using Luhn's Alg.
        Returns:
            bool
        """

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        checksum += sum(
            sum(digits_of(d*2)) for d in even_digits
        )
        return (checksum % 10) == 0

    @api.multi
    def _luhn_constrains_helper(self, col_name, country_col='country_id'):
        """ Provide a mixer for luhn validation via constrain
        Params:
            col_name: ``str`` Name of db column to constrain
            country_col: ``str`` Name of db country column to verify
        Raises:
            ValidationError: If constrain is a failure
            AttributeError: If country column is not valid or is null in db
        """

        for rec_id in self:
            if getattr(rec_id, country_col).code == 'US':
                if not self._luhn_is_valid(
                    getattr(rec_id, col_name, 0)
                ):
                    col_obj = self.env['ir.model.fields'].search([
                        ('name', '=', col_name),
                        ('model', '=', rec_id._name),
                    ],
                        limit=1,
                    )
                    raise ValidationError(
                        'Invalid %s was supplied.' % col_obj.display_name
                    )
