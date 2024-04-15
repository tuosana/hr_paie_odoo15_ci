# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Comptabilisation des emprunts",
    'version': '1.0',
    'category': 'Human Resources/Loans',
    'description': """
Add all information on the employee form to manage loans/AVS.
=============================================================

    * Loans
    * AVS

You can assign several loans and avs per employee.
    """,
    'author': "KERYATEC",
    'website': 'https://www.keryatec.com',
    'depends': ['hr_emprunt', 'hr_payroll'],
    'data': [
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
