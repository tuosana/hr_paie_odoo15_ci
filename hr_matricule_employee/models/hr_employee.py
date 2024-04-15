# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            vals['identification_id'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('hr.employee') or _('N/A')
        else:
            vals['identification_id'] = self.env['ir.sequence'].next_by_code('hr.employee') or _('N/A')
        print(vals)
        result = super(HrEmployee, self).create(vals)
        return result

    cni_number = fields.Char("N° carte d'identité", required=False)