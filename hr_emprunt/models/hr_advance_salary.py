# -*- coding:utf-8 -*-


from odoo import api, models, fields, exceptions


class HrAdvanceSalary(models.Model):
    _name = 'hr.advance.salary'
    _order = 'id desc'

    name = fields.Char('Designation')
    employee_id = fields.Many2one('hr.employee', 'Employé', required=True)
    date = fields.Date("Date", required=True)
    state = fields.Selection(
        [('draft', 'Brouillon'), ('submit', 'Soumis aux RH'), ('done', 'Validé'), ('cancel', 'Annulé'),
         ('reject', 'Rejeté')], 'Status', default='draft')
    amount = fields.Integer('Montant', required=True)
    company_id = fields.Many2one('res.company', 'Société', default=lambda self: self.env.user.compnay_id.id)

    def action_draft(self):
        for res in self:
            res.state = 'draft'

    def action_submit(self):
        for res in self:
            res.state = 'submit'

    def action_done(self):
        for res in self:
            res.state = 'done'

    def action_cancel(self):
        for res in self:
            res.state = 'cancel'

    def action_reject(self):
        for res in self:
            res.state = 'reject'
