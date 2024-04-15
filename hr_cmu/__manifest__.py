##############################################################################
#
# Copyright (c) 2012 KERYATEC - jonathan.arra@keryatec.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_cmu
# ##############################################################################
{
    "name": "Couverture maladie universelle Côte d'Ivoire",
    "version": "1.0",
    "author": "Jean Jonathan ARRA(KERYATEC)",
    'category': 'Localization',
    "website": "http://www.keryatec.com",
    #"depends": ["base", 'hr_update', 'hr_payroll_ci'],
    "depends": ["base",'hr_update','hr_payroll'],
    "description": """
    """,
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_view.xml",
    ],
    "installable": True
}
