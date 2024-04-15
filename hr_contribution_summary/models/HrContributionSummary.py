# -*- encoding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2015 - SIIGCI - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_payroll_ci_raport
# ##############################################################################


from odoo import fields, models


class HrContributionCompany(models.Model):
    _name = 'hr.contribution.company'

    name = fields.Char('Libellé', required=True)
    type = fields.Selection([('impot', 'Impôts'), ('cotisation', 'Cotisations'), ('assurance', 'Mutelle')],
                            'Type de contribution', default=False)
    employee_rule_ids = fields.Many2many('hr.salary.rule', 'contribution_employee_rule','contribution_id', 'rule_id',
                                         domain="[('type_rule','=', type)]", string="Règles salariales part employé")
    employer_rule_ids = fields.Many2many('hr.salary.rule', 'contribution_employer_rule','contribution_id', 'rule_id',
                                         domain="[('type_rule','=', type)]", string="Règles salariales part employeur")
    plafond = fields.Float('Plafond')
    company_id = fields.Many2one("res.company", "Société", default=lambda self: self.env.company)