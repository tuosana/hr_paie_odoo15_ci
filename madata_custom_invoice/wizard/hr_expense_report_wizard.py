from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class CommerceRapport(models.TransientModel):
    _name = 'hr.expense.report.wizard'
    _description='reporting notes de frais'

    employee_id = fields.Many2many('hr.employee', string='Employé')
    date_debut = fields.Date(string='Date du debut')
    date_fin = fields.Date(string='Date de la fin')
    employee_name=fields.Text("Name employé")


    payment_mode = fields.Selection([
        ("company_account", "Demande"),
        ("own_account", "Remboursement")
    ], tracking=True, string="Notes de frais")

    state = fields.Selection([
        ('draft', 'Accepté par le responsable'),
        ('approved', 'Confirmé par le comptable'),
    ], string='État', tracking=True)
       
# access_hr_expense_report_wizard,hr.expense.report.wizard,model_hr_expense_report_wizard,base.group_user,1,1,1,1

    def action_print_reporting(self):
        domain=[]
        # employee_id=self.employee_id
        if self.employee_id:
            domain += [('employee_id' , 'in', self.employee_id.mapped('id'))]
            self.employee_name=str(self.employee_id.mapped('name')).replace("'","").replace('[','').replace(']','')


        date_debut=self.date_debut
        if date_debut:
            domain += [('date' , '>=', date_debut)]

        date_fin=self.date_fin
        if date_fin:
            domain += [('date' , '<=', date_fin)]
        
        if self.payment_mode=='company_account':
            domain += [('payment_mode' , '=', self.payment_mode)]

        if self.payment_mode=='own_account':
            domain += [('payment_mode' , '=', self.payment_mode)]

        if self.state=='draft':
            domain += [('state' , '=', self.state)]

        if self.state=='approved':
            domain += [('state' , '!=','draft')]              

        notes_frais = self.env['hr.expense'].search_read(domain)

        data={
            'form_data': self.read()[0],
            'notes_frais':notes_frais
        }
        return self.env.ref('madata_custom_invoice.action_report_hr_expense_wizard').report_action(self, data=data)
