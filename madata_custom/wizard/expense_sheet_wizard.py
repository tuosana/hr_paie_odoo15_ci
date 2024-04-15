# _*_ coding : utf-8 _*_
from datetime import datetime, time
from odoo import api, fields, models

 

class ExpenseSheetWizard(models.TransientModel):
    _name = 'expense.sheet.wizard'
    _description = 'Creation du pop Up avec Wizard'

    start_date = fields.Date(string="Date debut")
    end_date = fields.Date(string="Date fin")
    filtre_employee = fields.Selection([
        ('one', 'Employé'),
        ('all', 'Tous les employés'),
    ], string='Trier par', default='one')
    validite = fields.Selection([
        ('all', 'Tous'),
        ('valide', 'Validé'),
        ('non_valide', 'Non validé'),
    ], string='Demande', default='all')
    # employee_id = fields.Many2one("hr.employee", string='Employé')
    employee_id = fields.Many2many("hr.employee", string='Employé', context={'active_test': False})
    expense_ids = fields.Many2one("hr.expense", string='Depenses')
    etat = fields.Selection([
        ('demande', 'Demande'),
        ('rembourse', 'Remboursement'),
        ('all', 'Remboursement et demande'),
    ], string='Type', default='all')


    def action_cancel(self):
        return False
    
    def report_expense_fonc(self):
        dic = []
        employee_id = self.employee_id
        if employee_id and self.filtre_employee=='one':
            # dic += [("employee_id", "=", employee_id.id)]
            dic += [("employee_id", "in", employee_id.mapped('id'))]
        start_date = self.start_date
        if start_date:
            dic += [("date", ">=", start_date)]
        end_date = self.end_date
        if end_date:
            dic += [("date", "<=", end_date)]

        validite = self.validite
        if validite == 'valide':
            dic += [("state", "in", ["approved","done"])]
        elif validite=='non_valide':
            dic += [("state", "in", ["draft","reported","refused"])]
        else:
            pass

        etat = self.etat
        if etat == 'demande':
            dic += [("payment_mode","=", "company_account")]
        elif etat == 'rembourse':
            dic += [("payment_mode", "=", "own_account")]
        else:
            dic += [("payment_mode", "in", ["company_account","own_account"])]

        
        note_frais = self.env["hr.expense"].search_read(dic)
        data_db = {
            "form" : self.read()[0],
            "note_frais" : note_frais
        }
        # return self.env.ref('madata_custom.report_hr_expense_wizard').report_action(self)
        return self.env.ref('madata_custom.report_hr_expense_wizard').report_action(self, data=data_db)







