# -*- coding:utf-8 -*-

from odoo import fields, api, models, _
from dateutil import relativedelta
from datetime import date


class hrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def compute_holidays_auto(self):
        this_date = date.today()
        type = self.env['hr.leave.type'].search([('code', '=', 'CONG')], limit=1)
        if type:
            for emp in self.search([]):
                temp_date = fields.Date.from_string(emp.start_date) + relativedelta.relativedelta(month=this_date.month,
                                                                                          year=this_date.year)
                if temp_date == this_date:
                    print("Employé %s est venu le %s",(emp.name, emp.start_date))
                    name = 'Attribution congés annuels de %s-%s' % (this_date.month, this_date.year)
                    vals = {
                        'name': name,
                        'employee_id': emp.id,
                        'holiday_status_id': type.id,
                        'allocation_type': 'regular',
                        'holiday_type': 'employee',
                        'company_id': emp.company_id.id,
                    }
                    if emp.nature_employe == 'local':
                        print(emp.company_id.number_holidays_locaux)
                        vals['number_of_days'] = emp.company_id.number_holidays_locaux
                        # vals['number_of_days_display'] = emp.company_id.number_holidays_locaux
                        # vals['duration_display'] = emp.company_id.number_holidays_locaux
                    else:
                        print(emp.company_id.number_holidays_expat)
                        vals['number_of_days'] = emp.company_id.number_holidays_expat
                        # vals['number_of_days_display'] = emp.company_id.number_holidays_expat
                        # vals['duration_display'] = emp.company_id.number_holidays_expat
                    print(vals)
                    holidays = self.env['hr.leave.allocation'].create(vals)
                    # if holidays:
                    #     holidays.action_approve()
        return True
