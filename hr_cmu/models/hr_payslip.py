# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def _input_lines(self, contract_id, struct_id):
        input_lines = self.input_line_ids.browse([])
        if contract_id and struct_id:
            data_inputs = contract_id.get_inputs_payslip()
            if contract_id.employee_id.cmu_part != 0:
                type = self.env['hr.payslip.input.type'].search([('code', '=', 'CMU')], limit=1)
                if type:
                    val = {
                        'input_type_id': type.id,
                        'amount': contract_id.employee_id.cmu_part,
                        'contract_id': contract_id.id,
                        #'struct_id': struct_id.id
                    }
                    data_inputs.append(val)
            for r in data_inputs:
                input_lines |= input_lines.new(r)
            if struct_id.input_line_type_ids:
                intups_data = []
                for type in struct_id.input_line_type_ids:
                    val = {
                        'input_type_id': type.id,
                        'amount': 0,
                        'contract_id': contract_id.id,
                        #'struct_id': struct_id.id
                    }
                    intups_data.append(val)
                for r in intups_data:
                    input_lines |= input_lines.new(r)

            return input_lines
        else:
            return [(5, False, False)]