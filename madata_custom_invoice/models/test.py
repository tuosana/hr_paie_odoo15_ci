nbr_cal_notes_frais=fields.Float(string="", compute='_compute_nbr_cal_notes_frais', store=False)

    notes_frais=fields.Float(string="Notes de frais", compute='_compute_again', depends=["nbr_cal_notes_frais"])

    def _compute_nbr_cal_notes_frais(self):
        for rec in self:
            rec.nbj_calc_conge_restant = random.randint(0, 100)
            rec._compute_again()

    @api.depends('date_from','date_to','employee_id')
    @api.onchange('date_from','date_to','employee_id')
    def _compute_again(self):
        for rec in self:
            if rec.employee_id and rec.date_from and rec.date_to:
                self._cr.execute(f"""
                        select employee_id, coalesce(sum(total_amount),0) as notes_frais from hr_expense_sheet
                        where state = 'post'
                        and payment_state='not_paid' 
                        and employee_id=  {rec.employee_id.id} 
                        and accounting_date >= '{rec.date_from}'
                        and accounting_date <= '{rec.date_to}'
                        group by
                        employee_id""")
                
                hr_notes_frais=self._cr.dictfetchall()
                for hr_note_frais in hr_notes_frais:
                    if hr_note_frais['notes_frais']:
                        rec.notes_frais = hr_note_frais['notes_frais']

    
   




    self._cr.execute(f"""
                        select employee_id, coalesce(sum(total_amount),0) as notes_frais from hr_expense_sheet
                        where state = 'post'
                        and payment_state='not_paid' 
                        and employee_id=  {rec.employee_id.id} 
                        and accounting_date >= '{rec.date_from}'
                        and accounting_date <= '{rec.date_to}'
                        group by
                        employee_id""")



    hr_notes_frais=self._cr.dictfetchall()
                    for hr_note_frais in hr_notes_frais:
                        if hr_note_frais['notes_frais']:
                            rec.notes_frais = hr_note_frais['notes_frais']



    payment_modes=fields.Char("Payment mode", compute='_compute_payment_modes',depends=["nbr_cal_notes_frais"], store=True)


    def _compute_nbr_cal_notes_frais(self):
        for rec in self:
            rec.nbj_calc_conge_restant = random.randint(0, 100)
            rec._compute_payment_modes()

    @api.depends('employee_id')
    @api.onchange('employee_id')
    def _compute_payment_modes(self):
        for rec in self:
            rec.payment_modes=rec.payment_mode




nbr_cal_notes_frais=fields.Float(string="", compute='_compute_nbr_cal_notes_frais', store=False)

    amount_available=fields.Monetary("Montant disponible", compute='_compute_amount_available',depends=["nbr_cal_notes_frais"], store=True)

    amount_available=fields.Monetary("Montant disponible")


    def _compute_nbr_cal_notes_frais(self):
        for rec in self:
            rec.nbj_calc_conge_restant = random.randint(0, 100)
            rec._compute_amount_available()

    @api.depends('employee_id')
    @api.onchange('employee_id')
    def _compute_amount_available(self):
        datas=self.env['hr.expense'].search([('sheet_id','=',self.id)])
        self.amount_available=sum(datas.mapped('total_amount_company'))






def action_sheet_move_create(self):
        if  self.amount_withheld==0:
            if (self.amount_available - self.total_amount) != 0 and self.payment_mode=="company_account":
                raise UserError(_("Veuillez saisir le montant retenu"))
        
        res = super(HrExpenseSheet, self).action_sheet_move_create()
        return res
    


    nbr_cal_notes_frais=fields.Float(string="", compute='_compute_nbr_cal_notes_frais', store=False)

    amount_available_expense=fields.Monetary("Montant disponible", compute='_compute_amount_available',depends=["nbr_cal_notes_frais"], store=True)
    
    amount_available_retenu=fields.Monetary("Montant Retenu11", compute='_compute_amount_available',depends=["nbr_cal_notes_frais"], store=True)

    def _compute_nbr_cal_notes_frais(self):
        for rec in self:
            rec.nbj_calc_conge_restant = random.randint(0, 100)
            rec._compute_amount_available()

    @api.depends('employee_id', 'amount_available')
    @api.onchange('employee_id','amount_available')
    def _compute_amount_available(self):
        
        for rec in self:
            if  rec.amount_available !=0:
                    datas=self.env['hr.expense'].search([('sheet_id','=',rec.id)])
                    rec.amount_available_expense=sum(datas.mapped('total_amount_company'))
                    rec.amount_available_retenu= rec.amount_available - rec.amount_available_expense
            else:
                pass

    #@api.onchange('employee_id','amount_available')
    #def _employee_id(self):
    #    for rec in self:
    #        if  rec.amount_available !=0:
    #            rec.amount_withheld=rec.amount_available_retenu