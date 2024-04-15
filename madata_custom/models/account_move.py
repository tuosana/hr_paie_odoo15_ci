# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError
from num2words import num2words

class AccountMoveCustoms(models.Model):
    _inherit = "account.move"

    nu_c_contribuable=fields.Char(string='N. C. Contribuable', related='partner_id.code_cc', store=True)
    nu_c_client=fields.Char(string='N. C. Client', related='partner_id.nc_client', store=True)
    street=fields.Char(string='Adresse client', related='partner_id.street', store=True)
    street2=fields.Char(string='Adresse2 client', related='partner_id.street2', store=True)
    city=fields.Char(string='Ville du client', related='partner_id.city', store=True)

    votre_bc=fields.Char(string='Votre BC', store=True)
    objet=fields.Char(string='Objet', store=True)

    tva_suspendue=fields.Boolean(string='TVA Suspendue', default=False)

    tva_non_facture=fields.Integer(string='TVA non Facturée', compute='_compute_tva_non_facture')
    delai_a_reglement=fields.Char()

    
    @api.model
    def default_get(self,fields):
        res=super(AccountMoveCustoms,self).default_get(fields)
        if self.env.context.get('default_id_central'):
            res['id_central']=self.env.context.get('default_id_central')
            # res['journal_id']=15
            res['currency_id']=41
            # res['currency_id']=1
            # for rec in self:
            #     datas = self.env['centralisation.tva'].search([('id', '=', self.env.context.get('default_id_central'))])
            #     # move_lines = self.env['account.move.line'].sudo().create({
            #     # 				'location_dest_id': val.location_dest_id.id,
            #     # 				'origin': val.origin,
            #     # 				'location_id': val.location_id.id,   # Partner Locations/Customers
            #     # 				'picking_type_id': val.picking_type_id.id,
            #     # 				'partner_id': val.partner_id.id,
            #     # 				'sale_order_id': val.sale_order_id.id,
            #     # 				'ref_pl': val.name,
            #     # 				'state': 'draft',
            #     # 				'group_id': val.group_id,
            #     # 			})
            #     if datas:
                    
                        # acc_move = self.create({
                        #                 'name': rec.name,
                        #                 'currency_id': 1,
                        #                 'date': rec.date,
                        #                 # 'facture_acompte': rec.facture_acompte,
                        #                 'journal_id': rec.journal_id.id,
                        #                 'move_type': rec.move_type,
                        #                 'financial_type': rec.financial_type,
                        #                 'id_central': rec.id_central,
                        #                 'state': 'draft',
                        #             })
                        # move_lines_vente = self.create({
                        #                 'account_id': 521,
                        #                 'name': 'TVA facturée sur vente',
                        #                 'debit': datas.tva_vente,   # Partner Locations/Customers
                        #                 'credit': 0,
                        #                 'currency_id': 1,
                        #                 'move_id': acc_move.id,
                        #             })
                        # move_lines_achat = self.create({
                        #                 'account_id': 530,
                        #                 'name': 'T.V.A. récupérable sur achats',
                        #                 'debit': 0,   # Partner Locations/Customers
                        #                 'credit': datas.tva_achat,
                        #                 'currency_id': 1,
                        #                 'move_id': acc_move.id,
                        #             })
                        # if datas.tva_due > 0:
                        #     move_lines_central = self.create({
                        #                     'account_id': 526,
                        #                     'name': 'Etat, T.V.A. due',
                        #                     'debit': 0,   # Partner Locations/Customers
                        #                     'credit': datas.tva_due,
                        #                     'currency_id': 1,
                        #                     'move_id': acc_move.id,
                        #                 })
                        # else:
                        #     move_lines_central = self.create({
                        #                     'account_id': 528,
                        #                     'name': 'Etat, crédit de T.V.A. à reporter due',
                        #                     'debit': datas.tva_due,   # Partner Locations/Customers
                        #                     'credit': 0,
                        #                     'currency_id': 1,
                        #                     'move_id': acc_move.id,
                        #                 })
        return res

    id_central=fields.Integer(string='Id Centralisation')


    # @api.depends('posted_before', 'state', 'journal_id', 'date')
    # def _compute_name(self):
    #     if self.state == 'draft':
    #         self.name = '/'
    #     elif self.state == 'posted':
    #         if self.sequence.code:
    #             self.name = self.env['ir.sequence'].next_by_code(self.sequence.code)
    #         else:
    #             super(AccountMoveCustoms, self)._compute_name()

    # @api.depends('posted_before', 'state', 'journal_id', 'date')
    def action_post(self):
        # for rec in self:
        #     sql1="update centralisation_tva set state='done' where id=%s)" % (rec.id_central)
        #     self._cr.execute(sql1)
        #     self._cr.commit()
        # for rec in self:
        # if self.id_central > 0:
        #     # sql1="update centralisation_tva set ref_ecriture=%s,state='done' where id=%d)"  % (rec.name,rec.id_central)
        #     sql1="update centralisation_tva set state='done' where id=%s)" % (self.id_central)
        #     self._cr.execute(sql1)
        #     self._cr.commit()

        res = super(AccountMoveCustoms, self).action_post()

        sql1="update centralisation_tva set ref_ecriture='%s',state='done' where id=%d"  % (str(self.name),self.id_central)
        self._cr.execute(sql1)
        self._cr.commit()

        return res


    # def query(self):
    #     if self.id_central > 0:
    #         sql1="update centralisation_tva set ref_ecriture='%s',state='draft' where id=%d"  % ('',self.id_central)
    #         self._cr.execute(sql1)
    #         self._cr.commit()
        

    def unlink(self):
        # res = super(AccountMoveCustoms, self).unlink()
        if self.state =='draft':
            sql1="update centralisation_tva set ref_ecriture='%s',state='draft' where id=%d"  % ('',self.id_central)
            self._cr.execute(sql1)
            self._cr.commit()

        res = super(AccountMoveCustoms, self).unlink()

        # tree_view_id = self.env.ref('madata_custom.centralisation_tva_tree').ids
        # form_view_id = self.env.ref('stock.view_picking_form').ids   
        return res #super(AccountMoveCustoms, self).unlink()

        # return res

    def active_lettrage(self):
        self._cr.execute(f"""
                        UPDATE account_account
                        SET reconcile = true
                        WHERE reconcile = false 
                    """)
        self._cr.commit()


    # @api.depends('company_id')
    # @api.onchange('company\q\q_id')
    # def _my_context_id(self):
    #     # my_id_centralisation = self.env['ir.config_parameter'].sudo().get_param('madata_custom.my_id_centralisation')
    #     # Use the value of my_parameter in your code
    #     for rec in self:
    #         # rec.journal_id=rec.journal_id.code='ODS'
    #         rec.journal_id='10'

    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_tva_non_facture(self):
        for rec in self:
            if rec.amount_tax==0:
                rec.tva_non_facture=rec.amount_untaxed * 0.18
            else:
                rec.tva_non_facture=rec.amount_tax

    amount_totlal_in_words = fields.Char(
        string="Montant total en lettre",
        store=True,
        compute='_compute_amount_totlal_in_words'
    )

    
    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_amount_totlal_in_words(self):
        for rec in self:
            if rec.currency_id:
                rec.amount_totlal_in_words = rec.currency_id.amount_to_text(rec.amount_total)
            else:
                rec.amount_totlal_in_words = False

    
    tva_suspendue_facture=fields.Float(string='TVA non Facturée', compute='_compute_tva_suspendue_facture')

    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_tva_suspendue_facture(self):
        for rec in self:
            if rec.tva_suspendue==True:
                rec.tva_suspendue_facture=rec.amount_untaxed * 0.18
            else:
                rec.tva_suspendue_facture=rec.amount_tax

    # FONCTION DE CALCULER LE MONTANT TOTAL SUSPENDUE

    montant_total_suspendue=fields.Float(string='TVA non Facturée', compute='_compute_montant_total_suspendue')
    
    
    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')    
    def _compute_montant_total_suspendue(self):
        for rec in self:
            if rec.tva_suspendue==True:
                rec.montant_total_suspendue=rec.amount_untaxed * 0.18 + rec.amount_untaxed
            else:
                rec.montant_total_suspendue=rec.amount_untaxed

    # FONCTION QUI PERMET DE METTRE LE MONTANT TOTAL SUSPENDUE  EN LETTRE

    montant_total_suspendue_in_words = fields.Char(
        string="Montant total en lettre",
        # store=True,
        compute='_compute_montant_total_suspendue_in_words'
    )
    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_montant_total_suspendue_in_words(self):
        for rec in self:
            if rec.currency_id:
                # rec.montant_total_suspendue_in_words = rec.currency_id.amount_to_text(int(rec.montant_total_suspendue))
                rec.montant_total_suspendue_in_words = num2words (rec.montant_total_suspendue, lang='fr').capitalize()
            else:
                rec.montant_total_suspendue_in_words = False


    # FONCTION QUI PERMET DE METTRE LE MONTANT amount_total  EN LETTRE

    amount_totlal_in_words = fields.Char(
        string="Montant total en lettre",
        compute='_compute_amount_totlal_in_words'
    )
    @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    def _compute_amount_totlal_in_words(self):
        for rec in self:
            if rec.currency_id:
                rec.amount_totlal_in_words=num2words(rec.amount_total, lang='fr').capitalize()
            else:
                rec.amount_totlal_in_words = False
    
    
 # CALCUL DE LA FACTURE ACOMPTE
    
    # creer_facture_acompte=fields.Boolean(string='Créer une Facture Acompte', default=False)

    # facture_acompte = fields.Selection([
    #     ('percentage', 'Acompte (en pourcentage)'),
    #     ('fixed', "Acompte (en montant fixe)"),
    #     ], string='Facture Acompte', required=False,
    #     help="Une facture standard est émise avec toutes les lignes de commande prêtes à être facturées, \
    #     selon leur politique de facturation (en fonction de la quantité commandée ou livrée).")

    # acompte_pourcentage = fields.Float("Montant de l'acompte", digits='Account', help="Le pourcentage du montant à facturer à l'avance, hors taxes.")
    
    # acompte_montant_fixe = fields.Monetary("Montant de l'acompte (fixe)", help="Le montant fixe à facturer à l'avance, hors taxes.")

    # montant_acompte_payer=fields.Monetary(string="Montant de l'acompte", compute='_compute_montant_acompte_payer')

    # @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    # @api.onchange('acompte_pourcentage', 'acompte_montant_fixe')
    # def _compute_montant_acompte_payer(self):
    #     for rec in self:
    #         if rec.creer_facture_acompte == True and rec.facture_acompte == 'percentage':
    #             if rec.tva_suspendue==True:
    #                 rec.montant_acompte_payer=rec.montant_total_suspendue * rec.acompte_pourcentage * 0.01
    #             else:
    #                 rec.montant_acompte_payer=rec.amount_total * rec.acompte_pourcentage * 0.01
    #         elif rec.creer_facture_acompte==True and  rec.facture_acompte == 'fixed':
    #             rec.montant_acompte_payer=rec.acompte_montant_fixe
            
    #         else:
    #             rec.montant_acompte_payer=0
    
    
    # reste_montant_payer=fields.Monetary(string="Reste du Montant", compute='_compute_reste_montant_payer')
    
    # @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    # @api.onchange('montant_acompte_payer')
    # def _compute_reste_montant_payer(self):
    #     for rec in self:
    #         if rec.creer_facture_acompte == True and rec.tva_suspendue==False:
    #             rec.reste_montant_payer=rec.amount_total - rec.montant_acompte_payer
    #         else:
    #             rec.reste_montant_payer=0
    
    
    # reste_montant_payer_tva_suspendue=fields.Monetary(string="Reste Montant avec TVA Suspendue", compute='_compute_reste_montant_payer_tva_suspendue')

    # @api.depends('amount_untaxed', 'amount_tax', 'amount_total')
    # @api.onchange('montant_acompte_payer')
    # def _compute_reste_montant_payer_tva_suspendue(self):
    #     for rec in self:
    #         if rec.creer_facture_acompte == True and rec.tva_suspendue==True:
    #             rec.reste_montant_payer_tva_suspendue=rec.montant_total_suspendue - rec.montant_acompte_payer
    #         else:
    #             rec.reste_montant_payer_tva_suspendue=0
    # 
    
    def delete_donnee(self):

    #     self._cr.execute(f"""
    #                         DELETE FROM hr_expense_request WHERE id = 1
    #                     """)
    #     self._cr.commit()
        
    #     self._cr.execute(f"""
    #                         DELETE FROM hr_expense WHERE id = 1
    #                     """)
    #     self._cr.commit()

        # self._cr.execute(f"""
        #                     DELETE FROM account_bank_statement WHERE id > 237
        #                 """)
        # self._cr.commit()

        self._cr.execute(f"""
                            DELETE FROM account_move WHERE id=5
                         """)
        self._cr.commit()

        # self._cr.execute(f"""
        #                     DELETE FROM account_move_line WHERE move_id > 14
        #                 """)
        # self._cr.commit() 

class accountMoveLineApi(models.Model):
    _inherit = "account.move.line"

    product_tmpl_id = fields.Many2one('product.template', string='Products template')
    default_code=fields.Char(string='Numéro', related='product_id.default_code', store=True)

    @api.onchange('account_id')
    @api.depends('partner_id','journal_id')
    def gh(self):
        four = self.env['res.partner'].search([('id', '=', self.partner_id.id)])
        if four.type_f == 'local' and self.journal_id.code == 'FAC':
           self.account_id = 916
        elif four.type_f == 'local' and self.journal_id.code == 'FACTU':
            self.account_id = 702
        elif four.type_f == 'etranger' and self.journal_id.code == 'FAC':
            self.account_id = 917
        elif four.type_f == 'etranger' and self.journal_id.code == 'FACTU':
            self.account_id = 703
        # elif four.type_f == 'etranger':
        #     # self.account_id = 704
        #     if self.journal_id.code == 'FACTU':
        #         self.account_id = 916
        #     else:
        #         self.account_id = 917


            