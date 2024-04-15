# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 KERYATEC - support@keryatec.com
# Author: KERYATEC
#
# Fichier du module hr_contribution_summary
# ##############################################################################
{
    "name" : "Contribution summary",
    "version" : "1.0",
    "author" : "KERYATEC",
    'category': 'Human Resources',
    "website": "www.keryatec.com",
    "depends": ['base', "hr_payroll_ci"],
    "description": """ 
        Gestion des résumé de cotisationss tels que:
        - CNPS
        - ITS
        - Contribution National
        - IGR
        - CMU
        
    """,
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/rules_group.xml",
        "security/ir.model.access.csv",
        "views/hr_salary_rule_view.xml",
        "views/hr_contribution_summary_view.xml",
        "wizards/hrPayrollCotisationsummary_view.xml",
        "reports/report_menu_view.xml",
        "views/report_payroll_contribution_summary.xml"
    ],
    "installable": True
}
