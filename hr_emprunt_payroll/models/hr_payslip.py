# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _input_lines(self, contract_id, struct_id):
        res = super(HrPayslip, self)._input_lines(contract_id, struct_id)
        advance_salary = self.employee_id.getAdvancedSalaryMonthly(self.date_from, self.date_to)
        if advance_salary != 0:
            input = {
                'name': "Avance sur salaire",
                'code': "AVS",
                'contract_id': contract_id.id,
                'amount': advance_salary,
            }
        emprunts = self.employee_id.get_amount_emprunt(self.date_from, self.date_to)
        if emprunts != 0:
            input = {
                'name': "Emprunts à déduire",
                'code': "EMP",
                'contract_id': contract_id.id,
                'amount': emprunts,
            }
            print(input)