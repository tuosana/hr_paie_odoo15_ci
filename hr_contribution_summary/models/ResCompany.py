# -*- encoding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2015 - SIIGCI - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_payroll_ci_raport
# ##############################################################################


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    contribution_summary_ids = fields.Many2many('hr.contribution.company', string="Résumé des contributions",
                                                required=False)
