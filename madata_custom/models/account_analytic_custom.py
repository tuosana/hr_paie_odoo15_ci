from odoo import models, fields, api, tools,  _
# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random


class AxeAnalytique(models.Model):
    _name = "account.analytic.axe"
    _rec_name = 'axe'

    axe = fields.Char(string="Libellé")


class FamilleAnalytique(models.Model):
    _name = "account.analytic.family"
    _rec_name = "libelle"

    code = fields.Char(string="Code")
    libelle = fields.Char(string="Libellé")
    description = fields.Text(string="Observation")

    # axe_analytic = fields.Selection([
    #     ('ventes', 'Ventes'),
    #     ('depenses', 'Depenses'),
    #     ('frais_generaux', 'Frais généraux')
    # ], string='Axe analytique')
    account_analytic_axe = fields.Many2one('account.analytic.axe', string="Axe Analytique")



class GroupAnalyticCustom(models.Model):
    _inherit="account.analytic.group"

    code=fields.Char(string="Code")
    account_analytic_axe = fields.Many2one('account.analytic.axe', string="Axe Analytique")
    account_analytic_family = fields.Many2one('account.analytic.family', string="Famille de comptes analytiques")


class NatureAnalyticCustom(models.Model):
    _inherit="account.analytic.account"

    # code=fields.Char(string="Code")
    account_analytic_axe = fields.Many2one('account.analytic.axe', string="Axe Analytique")
    account_analytic_family = fields.Many2one('account.analytic.family', string="Famille de comptes analytiques")





    



