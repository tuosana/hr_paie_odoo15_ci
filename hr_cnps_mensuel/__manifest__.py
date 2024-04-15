# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Veone - support.veone.net
# Author: Veone
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name": "CNPS Mensuel",
    "version": "1.0",
    "author": "Jean-Jonathan ARRA",
    'category': 'Human Resources',
    "website": "",
    "depends": ['base', 'hr_payroll_ci', 'report_xlsx'],
    "description": """ 
    Gestion de la CNPS mensuelle
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [

        ],
    "data": [
        "security/group_view.xml",
        "security/ir.model.access.csv",
        "data/hr_cnps_settings.xml",
        "views/hrCnpsSettingsView.xml",
        "views/hrCnpsMonthlyView.xml",
        "reports/report_cnps_monthly.xml",
        "reports/report_menu.xml",
    ],
    "installable": True
}
