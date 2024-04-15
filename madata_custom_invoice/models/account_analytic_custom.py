from odoo import models, fields, api, tools,  _
# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random


class AccountAnalyticCustom(models.Model):
    _inherit="account.analytic.account"



class AccountAnalyticCustom(models.Model):
    _inherit="account.analytic.group"

    code=fields.Char(string="Code")
    account_analytic_family = fields.Many2one('account.analytic.family', string="Famille de comptes analytiques")



class familleAnalytique(models.Model):
    _name = "account.analytic.family"
    _rec_name = 'libelle'

    code = fields.Char(string="Code")
    libelle = fields.Char(string="Libellé")
    description = fields.Text(string="Observation")

    axe_analytic = fields.Selection([
        ('ventes', 'Ventes'),
        ('depenses', 'Depenses'),
        ('frais_generaux', 'Frais généraux')
    ], string='Axe analytique')

    # def action_uninstall(self):
    #     self.env['ir.module.module'].search([('name', '=', 'hr_payroll')]).button_immediate_uninstall()
    
    def action_uninstall(self):
        modules = self.env['ir.module.module'].search([('name', '=', 'hr_payroll')])
        return modules.button_immediate_uninstall()

    



