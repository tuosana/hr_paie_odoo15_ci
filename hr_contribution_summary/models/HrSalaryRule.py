# -*- encoding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2015 - KERYATEC - jonathan.arra@KERYATEC.com
# Author: Jean Jonathan ARRA
#
# Fichier du module HR_CONTRIBUTION_SUMMARY
# ##############################################################################


from odoo import fields, models


class HrPayslipSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'
    _order = 'sequence'

    type_rule = fields.Selection([('normal', 'Normal'), ('impot', 'Impôt'), ('cotisation', 'Cotisation'),
               ('assurance', 'Assurance')], default='normal', string='Type de règle')

