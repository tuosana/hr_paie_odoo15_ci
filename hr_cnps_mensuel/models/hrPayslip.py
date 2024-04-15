# -*- coding:utf-8 -*-

from odoo import api, fields, _, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.one
    def _get_tranche(self):
        type = 'm'
        if self.type != 'm':
            type = 'j'
        result = self.env['hr.cnps.setting'].search([('type', '=', '')])

    tranche_id = fields.Many2one('hr.cnps.setting', 'Tranche', compute='_get_tranche', store=True)