# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{

    'name': 'Medical Pharmacy - US Locale',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Medical Team, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'medical_base_us',
        'medical_pharmacy',
    ],
    'data': [
        'security/is.model.access.csv',
    ],
    "website": "https://laslabs.com",
    "licence": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
