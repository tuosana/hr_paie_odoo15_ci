# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError,UserError,ValidationError
from datetime import date, time, datetime, timedelta
import random

class HrPayslip(models.Model):
    _inherit = 'hr.employee'

    nbj_calc_conge_restant=fields.Float(string="", compute='_compute_nbr_conge', store=False)
    
    nbj_acquis=fields.Float(string="Nbj de congés aquis", compute='_compute_again', depends=["nbj_calc_conge_restant"], sorte=True)
    nbj_pris=fields.Float(string="Nbj de congés pris", compute='_compute_again', depends=["nbj_calc_conge_restant"], sorte=True)
    nbj_restants=fields.Float(string="Nbj de congés restants", compute='_compute_again', depends=["nbj_calc_conge_restant"], sorte=True)
    nbh_travailler=fields.Float(string="Nbh travailler", compute='_compute_again', depends=["nbj_calc_conge_restant"], sorte=True)

    last_three_leaves=fields.Text(string="3 dernieres conges", compute='_compute_again', depends=["nbj_calc_conge_restant"], sorte=True)


    def _compute_nbr_conge(self):
        for rec in self:
            rec.nbj_calc_conge_restant = random.randint(0, 100)
            rec._compute_again()
    
    def _compute_again(self):
        for rec in self:
            # rec.nbj_acquis=float(rec.allocation_display)
            # rec.nbj_pris = float(rec.allocation_used_display)
            # rec.nbj_restants= rec.nbj_acquis - rec.nbj_pris
            # rec.nbh_travailler=float(rec.hours_last_month_display)
            rec.nbh_travailler = 0

            self._cr.execute(f"""
                            select employee_id, coalesce(sum(number_of_days),0) as nbj_pris from hr_leave
                            where state = 'validate'
                            and holiday_status_id=1 and employee_id= {rec.id}
                            group by
                            employee_id""")
            
            holidays_nbj_pris=self._cr.dictfetchall()

            for holiday_nbj_pris in holidays_nbj_pris:
                if holiday_nbj_pris['nbj_pris']:
                    rec.nbj_pris = holiday_nbj_pris['nbj_pris']
            
            self._cr.execute(f"""
                            select employee_id, coalesce(sum(number_of_days),0) as nbj_acquis from hr_leave_allocation
                            where state = 'validate'
                            and holiday_status_id=1 and employee_id= {rec.id}
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
                            where state = 'validate' and date_to < current_date and holiday_status_id = 1 and employee_id = {rec.id}
                            order by date_to desc limit 3 offset 0""")

            rec.last_three_leaves=str(self._cr.dictfetchall()).replace("'",'"')


    contract_ids = fields.One2many("hr.contract", 'employee_id', string = "Contract")
    leave_ids = fields.One2many("hr.leave", 'employee_id', string = "Congés")
    today = fields.Date(compute = '_date_today')    
    civilite = fields.Selection(selection=[
        ('monsieur', 'Monsieur'),
        ('madame', 'Madame'),
        ('mademoiselle', 'Mademoiselle')], string='Civilité')
    manager_job = fields.Many2one(related='leave_manager_id.manager_job', string="Job manager")



    def _date_today(self):
        self.today = fields.Datetime.now()


class hrLeaveInherit(models.Model):
    _inherit = "hr.leave"

    date_repris = fields.Date(string='Date de réprise')
    # date_repris = fields.Date(string='Date de réprise', compute = '_prochain_jour_ouvrable')
    today = fields.Date(compute = '_date_today') 


    def print_conges(self):
        return self.env.ref('madata_custom.report_attestation_conges').report_action(self)
    
   
    def _date_today(self):
        self.today = fields.Datetime.now()

    
    @api.depends('request_date_to')
    @api.onchange('request_date_to')
    def _prochain_jour_ouvrable(self):
        if self.request_date_to:
            j_depart = self.request_date_to.weekday()
            if j_depart == 5:
                self.date_repris = self.request_date_to + timedelta(days=2)
            elif j_depart == 4:
                self.date_repris = self.request_date_to + timedelta(days=3)
            else:
                self.date_repris = self.request_date_to + timedelta(days=1)


class ResUsersInherit(models.Model):
    _inherit=('res.users')

    manager_job = fields.Many2one(related='employee_id.job_id') 
