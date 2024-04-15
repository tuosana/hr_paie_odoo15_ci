from odoo import models, fields, api, tools,  _
# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random
from odoo.exceptions import UserError


class HrPayslipCustom(models.Model):
    _inherit='hr.payslip'

    nbj_acquis=fields.Float(string="Nbj de congés aquis", default=0, compute='_compute_again', store=True)
    nbj_pris=fields.Float(string="Nbj de congés pris", default=0, compute='_compute_again', store=True)
    nbj_restants=fields.Float(string="Nbj de congés restants", default=0, compute='_compute_again', store=True)
    nbh_travailler=fields.Float(string="Nbh travailler", compute='_compute_again', store=True)
    last_three_leaves=fields.Text(string="3 dernieres conges", compute='_compute_again', default='[]', store=True)

    notes_frais=fields.Float(string="Notes de frais", default=0, store=True)

    notes_frais_retenu=fields.Float(string="Notes de frais retenu", default=0, store=True)


    @api.model
    def _compute_again1(self):
        for rec in self:
            rec.notes_frais_retenu=rec.employee_id.id



    @api.model
    @api.depends('date_from','date_to','employee_id')
    @api.onchange('date_from','date_to','employee_id')
    def _compute_again(self):
        for rec in self:
            if rec.employee_id and rec.date_from and rec.date_to:
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
        

    @api.depends('date_from','date_to','employee_id')
    @api.onchange('date_from','date_to','employee_id')
    def _employee_id(self):
        if self.employee_id:
            self._cr.execute(f"""
                    select hes.employee_id, coalesce(sum(hes.total_amount),0) as notes_frais from hr_expense_sheet hes, hr_expense he
                    where he.sheet_id=hes.id
                    and hes.state = 'post'
                    and hes.payment_state='not_paid' 
                    and he.payment_mode='own_account'
                    and hes.notes_frais_r_g='true'
                    and hes.employee_id= {self.employee_id.id}
                    and hes.accounting_date >= '{self.date_from}'
                    and hes.accounting_date <= '{self.date_to}'
                    group by
                    hes.employee_id
                    """)
                    
            hr_notes_frais=self._cr.dictfetchall()
            for hr_note_frais in hr_notes_frais:
                noteg=[]
                if hr_note_frais['notes_frais']:
                    self.notes_frais = hr_note_frais['notes_frais']
                    noteg.append((0, 0,{
                        'name':'Note de frais(Gain)',
                        'code':'NOTEFG',
                        'amount':hr_note_frais['notes_frais'],
                        'contract_id':self.contract_id.id,
                        'payslip_id':self.id
                    }))
                self.update({'input_line_ids':noteg})
                    
            
            self._cr.execute(f"""
                    select hes.employee_id, coalesce(sum(hes.amount_withheld),0) as notes_frais_retenu from hr_expense_sheet hes, hr_expense he
                    where he.sheet_id=hes.id
                    and hes.state = 'done'
                    and hes.payment_state='paid' 
                    and amount_already_withheld=0
                    and he.payment_mode='company_account'
                    and hes.notes_frais_r_g='true'
                    and hes.employee_id= {self.employee_id.id}
                    and hes.accounting_date >= '{self.date_from}'
                    and hes.accounting_date <= '{self.date_to}'
                    group by
                    hes.employee_id
                    """)
                        
            hr_notes_frais=self._cr.dictfetchall()
            for hr_note_frais in hr_notes_frais:
                noter=[]
                if hr_note_frais['notes_frais_retenu']:
                    self.notes_frais_retenu = hr_note_frais['notes_frais_retenu']
                    noter.append((0, 0,{
                        'name':'Note de frais(Retenue)',
                        'code':'NOTEFR',
                        'amount':hr_note_frais['notes_frais_retenu'],
                        'contract_id':self.employee_id.contract_id,
                        'payslip_id':self.id
                    }))
                self.update({'input_line_ids':noter})                    

            

    def action_payslip_done(self):
        if self.notes_frais != 0:
            self._cr.execute(f"""
                                UPDATE hr_expense_sheet
                                SET state = 'done', payment_state='in_payment'
                                WHERE employee_id=  {self.employee_id.id} 
                                and payment_state='not_paid' 
                                and state='post'
                                and notes_frais_r_g='true'
                                and accounting_date >= '{self.date_from}'
                                and accounting_date <= '{self.date_to}'
                            """)
            self._cr.commit()
        
        if self.notes_frais_retenu != 0:
            self._cr.execute(f"""
                                UPDATE hr_expense_sheet
                                SET amount_already_withheld=amount_withheld
                                WHERE employee_id=  {self.employee_id.id}
                                and payment_state='paid' 
                                and state='done'
                                and amount_already_withheld=0
                                and notes_frais_r_g='true'
                                and accounting_date >= '{self.date_from}'
                                and accounting_date <= '{self.date_to}'
                            """)
            self._cr.commit()
        

        res = super(HrPayslipCustom, self).action_payslip_done()
        return res


    

    




