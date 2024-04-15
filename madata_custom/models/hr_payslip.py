# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # @api.onchange('employee_id')
    # def get_employee_work_days_data(self, employee_id, date_from, date_to):
    #     # Get the employee's contract
    #     contract = self.env['hr.contract'].search([('employee_id', '=', employee_id)], limit=1)

    #     # Get the work days data for the contract
    #     work_days_data = self.get_work_days_data(date_from, date_to, contract_id=contract.id)

    #     return work_days_data

    # @api.onchange('employee_id')
    # def get_employee_inputs(self, employee_id, date_from, date_to):
    #     # Get the employee's contract
    #     contract = self.env['hr.contract'].search([('employee_id', '=', employee_id)], limit=1)

    #     # Get the inputs for the contract
    #     inputs = self.get_inputs(contract, date_from, date_to)

    #     return inputs

    nbj_acquis=fields.Float(string="Nbj de congés aquis", compute='_compute_again', store=True)
    nbj_pris=fields.Float(string="Nbj de congés pris", compute='_compute_again', store=True)
    nbj_restants=fields.Float(string="Nbj de congés restants", compute='_compute_again', store=True)
    last_three_leaves=fields.Text(string="3 dernieres conges", compute='_compute_again', store=True)
    

    @api.model
    @api.depends('date_to','employee_id')
    @api.onchange('date_to','employee_id')
    def _compute_again(self):
        for rec in self:
            if rec.employee_id:
                self._cr.execute(f"""
                                select employee_id, coalesce(sum(number_of_days),0) as nbj_pris from hr_leave
                                where state = 'validate'
                                and holiday_status_id=1 and employee_id= {rec.employee_id.id} and date_to <= '{rec.date_to}'
                                group by
                                employee_id""")
                
                holidays_nbj_pris=self._cr.dictfetchall()

                for holiday_nbj_pris in holidays_nbj_pris:
                    if holiday_nbj_pris['nbj_pris']:
                        rec.nbj_pris = holiday_nbj_pris['nbj_pris']
                
                self._cr.execute(f"""
                                select employee_id, coalesce(sum(number_of_days),0) as nbj_acquis from hr_leave_allocation
                                where state = 'validate'
                                and holiday_status_id=1 and employee_id= {rec.employee_id.id} and date_from <= '{rec.date_to}'
                                group by
                                employee_id""")
                
                holidays_nbj_acquis=self._cr.dictfetchall()
                for holiday_nbj_acquis in holidays_nbj_acquis:
                    if holiday_nbj_acquis['nbj_acquis']:
                        rec.nbj_acquis = holiday_nbj_acquis['nbj_acquis']
                
                rec.nbj_restants = rec.nbj_acquis - rec.nbj_pris

                self._cr.execute(f"""
                            select id, to_char(date_from,'DD-MM-YYYY') as date_from, 
                            to_char(date_to,'DD-MM-YYYY') as date_to
                            from hr_leave
                            where state = 'validate' and holiday_status_id = 1 and employee_id = {rec.employee_id.id} and date_to <= '{rec.date_to}'
                            order by date_to desc limit 3 offset 0 """)

                rec.last_three_leaves=str(self._cr.dictfetchall()).replace("'",'"')



    # @api.depends('employee_id','date_to')
    # @api.onchange('employee_id','date_to')
    # def _compute_last_3_leaves(self):
    #     if self.employee_id:
    #         self._cr.execute(f"""
    #                             select id, to_char(date_from,'DD-MM-YYYY') as date_from, 
    #                             to_char(date_to,'DD-MM-YYYY') as date_to
    #                             from hr_leave
    #                             where state = 'validate' and date_to < '{str(self.date_to)}' and holiday_status_id = 1 and employee_id = {int(self.employee_id.id)}
    #                             order by date_to desc limit 3 offset 0""")

    #         self.last_three_leaves=str(self._cr.dictfetchall()).replace("'",'"')

            



    @api.onchange('employee_id','date_from','date_to')
    def onchange_employee_id(self):
        if self.employee_id:
            self.worked_days_line_ids = [(5, 0, 0)]  # Remove existing workdays
            self.input_line_ids = [(5, 0, 0)]  # Remove existing inputs

            # Get the employee's contract
            contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)], limit=1)

            # Get the work days data from the contract
            # work_days_data = contract.get_work_days_data(self.date_from, self.date_to)
            # for rec in self:

            #     paydatas = self.create({
            #                     'employee_id': rec.employee_id.id,
            #                     'struct_id': rec.struct_id.id,
            #                     'contract_id': rec.contract_id.id,
            #                     'date_from': rec.date_from,
            #                     'date_to': rec.date_to,
            #                     'number': rec.number,
            #                     'credit_note': rec.credit_note,
                                
            #                 })

            if contract.struct_id.name == 'Mensuel':
                valeurs = []
            #     paydatas = self.create({
            # #                     'employee_id': rec.employee_id.id,
            # #                     'struct_id': rec.struct_id.id,
            # #                     'contract_id': rec.contract_id.id,
            # #                     'date_from': rec.date_from,
            # #                     'date_to': rec.date_to,
            # #                     'number': rec.number,
            # #                     'credit_note': rec.credit_note,
            #     })
                valeurs.append((0,0, {
                    'name': 'Jours Travaillés',
                    'code': 'WORK100',
                    'number_of_days': 30,
                    'number_of_hours': 173.33,
                    'rate': 100,
                    'contract_id': self.contract_id.id,
                    'payslip_id': self.id,
			    }))

                self.update({'worked_days_line_ids' : valeurs})
            
            # for rec in self:
            #     self.getAcquiredOnPeriod()
            #     self.getAcquiredLeave()

                # Jours de congés
                
                # res = []
                # congpayes = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
                # if congpayes.nbj_pris > 0:
                #     res.append((0,0, {
                #                 'name': 'Congés payés',
                #                 'code': 'GLOBAL',
                #                 'number_of_days': - congpayes.nbj_pris,
                #                 'number_of_hours': - ((congpayes.nbj_pris) * 8),
                #                 'rate': 100,
                #                 'contract_id': self.contract_id.id,
                #                 'payslip_id': self.id,
                #             }))
                #     self.update({'worked_days_line_ids' : res})


                res = []
                # self.env.cr.execute("select emp.id, hlt.name, sum(hla.number_of_days) as nbj_acquis, sum(hl.number_of_days) as nbj_pris, (sum(hla.number_of_days) - sum(hl.number_of_days))  as nbj_restants from hr_employee emp inner join hr_leave hl on emp.id = hl.employee_id inner join hr_leave_allocation hla on emp.id = hla.employee_id inner join hr_payslip hp on emp.id = hp.employee_id inner join hr_leave_type hlt on hl.holiday_status_id = hlt.id where hl.state = 'validate' and hl.date_from >= %s and hl.date_to <= %s and emp.id=%s and hl.holiday_status_id = 1 and hla.holiday_status_id = 1 group by emp.id, hlt.name",(str(self.date_from), str(self.date_to), self.employee_id.id))
                self.env.cr.execute("select hl.employee_id, hlt.name, coalesce(sum(hla.number_of_days),0) as nbj_acquis, coalesce(sum(hl.number_of_days),0) as nbj_pris, coalesce((sum(hla.number_of_days) - sum(hl.number_of_days)),0) as nbj_restants from hr_leave hl,hr_leave_allocation hla,hr_leave_type hlt where hl.employee_id=hla.employee_id and hl.holiday_status_id=hlt.id and hl.state = 'validate' and  hl.holiday_status_id=1 and hla.holiday_status_id=1 and hl.date_from >=%s and hl.date_to <=%s and hl.employee_id=%s group by hl.employee_id, hlt.name",(str(self.date_from), str(self.date_to), self.employee_id.id))
                # holidays = self._cr.dictfetchall()
                holidays = self.env.cr.dictfetchall()
                # print(holidays)
                # if holidays:
                for holiday in holidays:

                    # self.nbj_acquis=holiday['nbj_acquis']
                    # self.nbj_pris=holiday['nbj_pris']
                    # self.nbj_restants=holiday['nbj_restants']
                    # if holiday['nbj_pris'] > 0:
                    #     cong = []
                    #     cong.append((0,0, {
                    #             'name': 'Congés annuels ',
                    #             'code': 'CONGA',
                    #             'amount': 0,
                    #             'contract_id': self.contract_id.id,
                    #             'payslip_id': self.id,
                    #         }))
                    #     self.update({'input_line_ids' : cong})


                    res.append((0,0, {
                            'name': 'Congés payés',
                            'code': 'GLOBAL',
                            'number_of_days': - holiday['nbj_pris'],
                            'number_of_hours': - holiday['nbj_pris'] * 8,
                            'rate': 100,
                            'contract_id': self.contract_id.id,
                            'payslip_id': self.id,
                        }))
                self.update({'worked_days_line_ids' : res})

            self.env.cr.execute("select hl.employee_id, hlt.name, coalesce(hla.number_of_days,0) as nbj_acquis, coalesce(sum(hl.number_of_days),0) as nbj_pris, coalesce((hla.number_of_days - sum(hl.number_of_days)),0) as nbj_restants from hr_leave hl,hr_leave_allocation hla,hr_leave_type hlt where hl.employee_id=hla.employee_id and hl.holiday_status_id=hlt.id and hl.state = 'validate' and  hl.holiday_status_id=1 and hla.holiday_status_id=1 and hl.employee_id=%s group by hl.employee_id, hlt.name, hla.number_of_days" % (self.employee_id.id))
            holidays_acquired = self.env.cr.dictfetchall()
            for holiday_acquired in holidays_acquired:

                self.nbj_acquis=holiday_acquired['nbj_acquis']
                self.nbj_pris=holiday_acquired['nbj_pris']
                self.nbj_restants=holiday_acquired['nbj_restants']

                            # val = {
                            #     'name' : type_holiday.name,
                            #     'code' : type_holiday.code,
                            #     'number_of_days' : holiday['sum'],
                            #     'number_of_hours' : holiday['sum'] * 8,
                            # }
                            # res.append(val)



            # Gestion des inputs
            self.env.cr.execute("SELECT p.name,p.code,m.montant_prime,m.contract_id FROM hr_payroll_prime p,hr_payroll_prime_montant m WHERE m.prime_id=p.id and m.contract_id='%s'" % (int(contract.id)))
            datas = self.env.cr.dictfetchall()
            prime_lines = []
            vals = []

            input_obj = self.env['hr.payslip.input']
            
            for data in datas:	

                vals.append((0,0, {
			        'name' : data['name'],
                    'code' : data['code'],
                    'amount' : data['montant_prime'],
                    'contract_id' : data['contract_id'],
                    'payslip_id' : self.id,
			    }))
            self.update({'input_line_ids' : vals})
                
               
