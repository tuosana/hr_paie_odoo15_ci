from odoo import models, fields, api, tools,  _
from odoo.tools import email_split, float_is_zero, float_repr
from datetime import datetime, time, date

# from tools.translate import _
# from odoo.tools.amount_to_text_en import amount_to_text
import random
from odoo.exceptions import UserError, ValidationError

from  num2words import num2words

class HrExpense(models.Model):
    _inherit="hr.expense"
    request_id = fields.Many2one('hr.expense.request', string='Demande note de frais', domain=[('state', '=', 'done')])

    total_amount_orign = fields.Monetary(
        related='request_id.total_amount', store=True)
    
    @api.onchange('request_id')
    def _request_id(self):
        for rec in self:
            datas=self.env["hr.expense.request"].search([('id', '=', rec.request_id.id)])
            rec.name = datas.name
            rec.total_amount=datas.total_amount
            rec.product_id=datas.product_id
            rec.date=datas.date
            rec.employee_id=datas.employee_id
            rec.payment_mode=datas.payment_mode
            rec.description=datas.description


    # def action_submit_expenses(self):
        
    #     if self.total_amount_orign < self.total_amount:
    #         raise UserError(_("Veuillez saisir une somme inferieur ou égal à la somme mise à la disposition de l'employé et fait une demande de remboursement pour le surplus"))
    #     res = super(HrExpense, self).action_submit_expenses()

    #     if self.sheet_id:
    #         self._cr.execute(f"""
    #                         UPDATE hr_expense_sheet
    #                         SET amount_withheld=amount_available - total_amount 
    #                         WHERE employee_id={self.employee_id.id}
    #                         and id={self.sheet_id.id}
    #                         """)
    #         self._cr.commit()

    #     return res
    
    # def action_view_sheet(self):
        
    #     if self.total_amount_orign < self.total_amount:
    #         raise UserError(_("Veuillez saisir une somme inferieur ou égal à la somme mise à la disposition de l'employé et fait une demande de remboursement pour le surplus"))
    #     res = super(HrExpense, self).action_view_sheet()
    #     if self.sheet_id:
    #         self._cr.execute(f"""
    #                         UPDATE hr_expense_sheet
    #                         SET amount_withheld=amount_available - total_amount 
    #                         WHERE employee_id={self.employee_id.id}
    #                         and id={self.sheet_id.id}
    #                         """)
    #         self._cr.commit()
    #     return res
    
    def unlink(self):
    
        # for expense in self:
            # if expense.state in ['done']:
        raise UserError(_('Les notes de frais validés ne peuvent pas être supprimé.'))

        res = super(HrExpense, self).unlink()
        return res
    



class HrExpenseSheet(models.Model):
    _inherit="hr.expense.sheet"
    
    # amount_available=fields.Monetary("Montant disponible", default=0)

    amount_withheld=fields.Monetary(string="Montant à retenir", store=True)

    amount_already_withheld=fields.Monetary("Montant dejà retenu", default=0)

    notes_frais_r_g= fields.Boolean(string = "Active", default=True)

    amount_available = fields.Monetary("Montant disponible", currency_field='currency_id', compute='_compute_amount_available', store=True, tracking=True)

    # name = fields.Char('Description', required=True, tracking=True)


    @api.depends('expense_line_ids.total_amount_orign')
    def _compute_amount_available(self):
        for sheet in self:
            sheet.amount_available = sum(sheet.expense_line_ids.mapped('total_amount_orign'))

    
    # @api.onchange('total_amount')
    # def _total_amount(self):
    #     if self.payment_mode=="company_account":
    #         if (self.amount_available - self.total_amount) > 0:
    #             self.amount_withheld= self.amount_available - self.total_amount

    def action_submit_sheet(self):

        if self.amount_available - self.total_amount > 0:
            self._cr.execute(f"""
                UPDATE hr_expense_sheet
                SET amount_withheld=amount_available - total_amount 
                WHERE employee_id={self.employee_id.id}
                and id={self.id}
                """)
            self._cr.commit()

        res = super(HrExpenseSheet, self).action_submit_sheet()
        self.approve_expense_sheets()

        return res
        

    def unlink(self):
        
        raise UserError(_('Les notes de frais validés ne peuvent pas être supprimé.'))

        res = super(HrExpense, self).unlink()
        return res

class HrExpenseRequest(models.Model):
    _name="hr.expense.request"

    def unlink(self):
        
        for expense in self:
            if expense.state in ['done']:
                raise UserError(_('Les notes de frais validés ne peuvent pas être supprimé.'))
            
        res = super(HrExpenseRequest, self).unlink()
        return res

    @api.model
    def _default_employee_id(self):
        employee = self.env.user.employee_id
        if not employee and not self.env.user.has_group('hr_expense.group_hr_expense_team_approver'):
            raise ValidationError(_('The current user has no related employee. Please, create one.'))
        return employee
    
    @api.model
    def _default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id')

    @api.model
    def _get_employee_id_domain(self):
        res = [('id', '=', 0)] # Nothing accepted by domain, by default
        if self.user_has_groups('hr_expense.group_hr_expense_user') or self.user_has_groups('account.group_account_user'):
            res = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]"  # Then, domain accepts everything
        elif self.user_has_groups('hr_expense.group_hr_expense_team_approver') and self.env.user.employee_ids:
            user = self.env.user
            employee = self.env.user.employee_id
            res = [
                '|', '|', '|',
                ('department_id.manager_id', '=', employee.id),
                ('parent_id', '=', employee.id),
                ('id', '=', employee.id),
                ('expense_manager_id', '=', user.id),
                '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id),
            ]
        elif self.env.user.employee_id:
            employee = self.env.user.employee_id
            res = [('id', '=', employee.id), '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id)]
        return res
    name = fields.Char('Description', compute='_compute_from_product_id_company_id', store=True, required=True, copy=True,
        states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'approved': [('readonly', False)], 'refused': [('readonly', False)]})
    date = fields.Date(readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'approved': [('readonly', False)], 'refused': [('readonly', False)]}, default=fields.Date.context_today, string="Date de demande")
    employee_id = fields.Many2one('hr.employee', compute='_compute_employee_id', string="Employé",
        store=True, required=True, readonly=False, tracking=True,
        states={'approved': [('readonly', True)], 'done': [('readonly', True)]},
        default=_default_employee_id, domain=lambda self: self._get_employee_id_domain(), check_company=True)
    product_id = fields.Many2one('product.product', string='Article', readonly=True, tracking=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'approved': [('readonly', False)], 'refused': [('readonly', False)]}, domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", ondelete='restrict')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=False, store=True, compute='_compute_currency_id', default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary("Montant demandé", compute='_compute_amount', store=True, currency_field='currency_id', tracking=True, readonly=False)
    payment_mode = fields.Selection([
        ("company_account", "Demande"),
        ("own_account", "Remboursement")
    ], default='company_account', tracking=True, string="Notes de frais")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirm', 'Soumis'),
        ('done', 'Accepté'),
        ('reject', 'Refusé'),
        ('cancel', 'Annulé'),
    ], string='Status', copy=False, index=True, readonly=True, default='draft', help="Status of the expense.")
    description = fields.Text('Notes...', readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]})
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    unit_amount = fields.Float("Prix unitaire", compute='_compute_from_product_id_company_id', default=0, store=True, required=True, copy=True, digits='Product Price')
    untaxed_amount = fields.Float("Subtotal", store=True, compute='_compute_amount_tax', digits='Account', copy=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True, string="UoM Category")
    product_has_cost =  fields.Boolean("Is product with non zero cost selected", compute='_compute_product_has_cost')
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', compute='_compute_from_product_id_company_id',
        store=True, copy=True, readonly=True,
        default=_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    quantity = fields.Float(required=True,string="Quantité", readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'approved': [('readonly', False)], 'refused': [('readonly', False)]}, digits='Product Unit of Measure', default=1)
   
    tax_ids = fields.Many2many('account.tax',
        compute='_compute_from_product_id_company_id', store=True, readonly=False,
        domain="[('company_id', '=', company_id), ('type_tax_use', '=', 'purchase'), ('price_include', '=', True)]", string='Taxes',
        help="The taxes should be \"Included In Price\"")

    label_total_amount_company = fields.Char(compute='_compute_label_total_amount_company')

    total_amount_company = fields.Monetary("Total", compute='_compute_total_amount_company', store=True, currency_field='company_currency_id')

    same_currency = fields.Boolean("Is currency_id different from the company_currency_id", compute='_compute_same_currency')
    company_currency_id = fields.Many2one('res.currency', string="Report Company Currency", related='company_id.currency_id', readonly=True)
    
    label_convert_rate = fields.Char(compute='_compute_label_convert_rate')

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'hr.expense'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense._origin.id, 0)

    @api.depends('product_id')
    def _compute_product_has_cost(self):
        for expense in self:
            expense.product_has_cost = bool(expense.product_id and expense.unit_amount)

    @api.depends('product_id', 'company_id')
    def _compute_from_product_id_company_id(self):
        for expense in self.filtered('product_id'):
            expense = expense.with_company(expense.company_id)
            expense.name = expense.name or expense.product_id.display_name
            if not expense.attachment_number or (expense.attachment_number and not expense.unit_amount) or (expense.attachment_number and expense.unit_amount and not expense.product_id.standard_price):
                expense.unit_amount = expense.product_id.price_compute('standard_price')[expense.product_id.id]
            expense.product_uom_id = expense.product_id.uom_id
            expense.tax_ids = expense.product_id.supplier_taxes_id.filtered(lambda tax: tax.price_include and tax.company_id == expense.company_id)  # taxes only from the same company

            
    @api.depends('total_amount', 'tax_ids', 'currency_id')
    def _compute_amount_tax(self):
        for expense in self:
           
            amount = expense.total_amount
            quantity = 1
            taxes = expense.tax_ids.compute_all(amount, expense.currency_id, quantity, expense.product_id, expense.employee_id.user_id.partner_id)
            expense.untaxed_amount = taxes.get('total_excluded')
    
   
    @api.depends_context('lang')
    @api.depends("company_currency_id")
    def _compute_label_total_amount_company(self):
        for expense in self:
            expense.label_total_amount_company = _("Total %s", expense.company_currency_id.name) if expense.company_currency_id else _("Total")

    @api.depends('date', 'total_amount', 'currency_id', 'company_currency_id')
    def _compute_total_amount_company(self):
        for expense in self:
            amount = 0
            if expense.same_currency:
                amount = expense.total_amount
            else:
                date_expense = expense.date or fields.Date.today()
                amount = expense.currency_id._convert(
                    expense.total_amount, expense.company_currency_id,
                    expense.company_id, date_expense)
            expense.total_amount_company = amount
    
    @api.depends('currency_id', 'company_currency_id')
    def _compute_same_currency(self):
        for expense in self:
            expense.same_currency = bool(not expense.company_id or (expense.currency_id and expense.currency_id == expense.company_currency_id))

    
    @api.depends('date', 'total_amount', 'currency_id', 'company_currency_id')
    def _compute_label_convert_rate(self):
        records_with_diff_currency = self.filtered(lambda x: not x.same_currency and x.currency_id)
        (self - records_with_diff_currency).label_convert_rate = False
        for expense in records_with_diff_currency:
            date_expense = expense.date or fields.Date.today()
            rate = expense.currency_id._get_conversion_rate(
                expense.currency_id, expense.company_currency_id, expense.company_id, date_expense)
            rate_txt = _('1 %(exp_cur)s = %(rate)s %(comp_cur)s', exp_cur=expense.currency_id.name, rate=float_repr(rate, 6), comp_cur=expense.company_currency_id.name)
            expense.label_convert_rate = rate_txt
    
    @api.depends('quantity', 'unit_amount', 'tax_ids', 'currency_id')
    def _compute_amount(self):
        for expense in self:
            if expense.unit_amount:
                taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.quantity, expense.product_id, expense.employee_id.user_id.partner_id)
                expense.total_amount = taxes.get('total_included')

    # Fonction de l'annulation de la demande
    def action_cancel(self):
        self.state = "cancel"
    
    # Fonction de confirmation de la demande
    def action_confirm(self):
        self.state = "confirm"

    # Fonction d'acception et l'insertion des information de la demande dans hr.expense  
    def action_validate(self):
        self.env['hr.expense'].sudo().create({
               'name':self.name,
               'request_id':self.id,
               'product_id':self.product_id.id,
               'total_amount':self.total_amount,
               'unit_amount':self.unit_amount,
               'total_amount_company':self.total_amount_company,
               'date':self.date,
               'employee_id':self.employee_id.id,
               'company_id':self.company_id.id,
               'currency_id':self.currency_id.id,
               'payment_mode':self.payment_mode,
               'quantity':self.quantity,
               'description':self.description,
               'state':'draft',
            })
        
        self.env['account.bank.statement'].sudo().create({
               'name':self.numero_seq,
               'libelle':self.name,
               'request_id':self.id,
               'journal_id':8,
               'date':datetime.now(),
               'state':'open',
            })
        a_bank_s=self.env['account.bank.statement'].search([('request_id', '=', self.id)])

        id_abs=0
        for a_bank in a_bank_s:
            id_abs += a_bank.id
            a_bank.balance_end_real=a_bank.balance_start - self.total_amount

        self.env['account.bank.statement.line'].sudo().create({
               'payment_ref':self.name,
               'statement_id':id_abs,
               'amount': - self.total_amount,
               'date':datetime.now(),
            })
        self.state = "done"

    # Fonction de refuser de la demande
    def action_reject(self):
        self.state = "reject"

    # Fonction de remettre la demande en brouillon 
    def action_recomfirm(self):
        self.state = "draft"

    # Fonction d'impression de la piece de caisse de la demande
    def print_piece_caisse_pdf(self):
        return self.env.ref('madata_custom_invoice.report_piece_caisse').report_action(self)
    

    montant_lettre= fields.Char(string='Montant', compute='_conv_montant_lettre')
    numero_seq= fields.Char(string='Séquence')

    # Fonction du montant en lettre 
    def _conv_montant_lettre(self):
        self.montant_lettre=num2words(int(self.total_amount_company), lang="fr").capitalize()
    
    # Fonction pour generer les sequenses 
    @api.model
    def create(self, vals):
        vals["numero_seq"] = self.env["ir.sequence"].next_by_code("hr.expense.request")
        sheet=super(HrExpenseRequest, self).create(vals)
        return sheet
    
    # attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')
    
    # def _compute_attachment_number(self):
    #     attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'hr.expense.request'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
    #     attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
    #     for expense in self:
    #         expense.attachment_number = attachment.get(expense._origin.id, 0)

    attachment = fields.Binary(string="Joindre le reçu", attachment=True)

    attachment_ids = fields.Many2many(
        'ir.attachment', 'hr_expense_request_ir_attachments_rel',
        'models_id', 'attachment_id', 'Attachments')
    