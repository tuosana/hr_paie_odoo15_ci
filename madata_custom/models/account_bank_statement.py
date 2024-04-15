from odoo import models, fields, api, tools,  _
# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random


class AccountBankStatement(models.Model):
    _inherit="account.bank.statement"
    

    numero_seq=fields.Char("Numero de note de frais")
    libelle=fields.Char("Libellé")
    request_id = fields.Many2one('hr.expense.request', string='Demande note de frais', domain=[('state', '=', 'done')])
     
    montant=fields.Monetary(string='Montant', compute='_calcule_montant')


    @api.model
    def _calcule_montant(self):
        for rec in self:
            amount=self.env["account.bank.statement.line"].search([('statement_id', '=', rec.id)])
            rec.montant=sum(amount.mapped('amount'))
