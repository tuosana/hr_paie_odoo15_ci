# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError

class accountBankStatementApi(models.Model):
    _inherit = "account.bank.statement"

    @api.onchange('balance_end')
    def amount_counts(self):
        if self.balance_end:
            self.balance_end_real = self.balance_end
            