from odoo import models, fields, api, tools,  _
from odoo.tools import email_split, float_is_zero, float_repr

# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random
from odoo.exceptions import UserError, ValidationError

class saleOrderApi(models.Model):
    _inherit = "sale.order"
    descri_cust = fields.Char(string='Description', readonly=True)
    ca_prev = fields.Monetary(string='CA prev', readonly=True)
    budget_achat = fields.Monetary(string='Budget achat', readonly=True)
    mont_prev = fields.Monetary(string='Montant achat', readonly=True)

    @api.onchange('amonut_total')
    def onchange_amount(self):
        for rec in self:
            rec.ca_prev=rec.amount_total
    