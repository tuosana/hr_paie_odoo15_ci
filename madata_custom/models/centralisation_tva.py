# -*- coding: utf-8 -*-

from odoo import api, fields, _, models
from odoo.exceptions import AccessError,UserError,ValidationError
from datetime import datetime,date
from odoo.http import request


class CentralisationTva(models.Model):
	_name = 'centralisation.tva'
	_rec_name = 'months'
	# _order = 'years desc'
	_order = 'from_date'

	from_date = fields.Date(string='Date Début',readonly=True,store=True)
	to_date = fields.Date(string='Date Fin',readonly=True,store=True)
	tva_achat = fields.Integer(string='TVA sur Achat', readonly=True,store=True)
	tva_vente = fields.Integer(string='TVA sur Vente', readonly=True,store=True)
	tva_due = fields.Integer(string='TVA Dûe/Reporter', readonly=True,store=True)

	nb_pending = fields.Integer(string='Nb pending',compute='_calc_nb_pending')

	state = fields.Selection([
        ('draft', 'Brouillon'),
        ('progress', 'En cours'),
        ('done', 'Fait'),
    ], required=False, default='draft')

	ref_ecriture = fields.Char(string='Ref. Ecriture', readonly=True)


	my_id_centralisation = fields.Char('Id Centralisation', config_parameter='madata_custom.my_id_centralisation')

	years = fields.Selection([(str(num), str(num)) for num in range((datetime.now().year)-10, (datetime.now().year) + ( 1 if  datetime.now().month != 1 else 0 ) )], default=str((datetime.now().year) - ( 1 if  datetime.now().month == 1 else 0 )), string='Année', required=True)
	months = fields.Selection([(('0'+(str(n))) if n in range(1, 10) else str(n), str(m)) for (n,m) in zip(range(1, 13),['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','decembre'][:12])], default='01',required=True)
	months_now = fields.Selection([('0'+(str(n)) if n in range(1, 10) else str(n), str(m)) for (n,m) in zip(range(1, datetime.now().month),['Janvier','Fevrier','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','decembre'][:datetime.now().month])], default='01',required=True)   
	nombre_annee=fields.Integer(string='Annee en cours', default=1, compute='_calcule_nombre_annee')
    
	jrs_fin = fields.Integer(string='Jours')
	# from_date = fields.Date(compute = '_from_date')
	# to_date = fields.Date(compute = '_to_date')
	conct_date = fields.Char(compute = '_conct_date')

	# @api.model
	# def _state_delete(self):
	# 	for rec in self:
	# 		req = self.env['account.move'].search([('id_central', '=', int(rec.id))])
	# 		if not req:
	# 			# sql1="update centralisation_tva set ref_ecriture='%s',state='draft' where id=%d"  % ('',rec.id)
	# 			# self._cr.execute(sql1)
	# 			# self._cr.commit()
	# 			self.write({
	# 			'ref_ecriture': '',
	# 			'state': 'draft'
	# 		})

	_sql_constraints = [
        ('unique_date_range',
         'UNIQUE(from_date, to_date)',
         'La période de centralisation doit être unique.')
    ]


	def _calc_nb_pending(self):
		for rec in self:
			req = self.env['centralisation.tva'].search_count([('state', '=', 'progress')])
			if req > 0:
				rec.nb_pending=1
			else:
				rec.nb_pending=0

	# @api.constrains('from_date', 'to_date')
	# def _check_unique_date_range(self):
	# 	for record in self:
	# 		if record.from_date and record.to_date:
	# 			# if self.search_count([('id', '!=', record.id), ('start_date', '<=', record.end_date), ('end_date', '>=', record.start_date)]):
	# 			# 	raise ValueError("A record already exists for this date range.")
	# 			if self.search_count([('from_date', '<=', record.to_date), ('to_date', '>=', record.from_date)]):
	# 				raise ValueError("La période de centralisation doit être unique.'")


	def action_centraliser(self):
		# print('Ok')
		
		# # tree_view_id = self.env.ref('madata_custom.achat_materiel_tree').ids
        # form_view_id = self.env.ref('stock.view_picking_form').ids   
        # return {
        #     'name':_('PL à Faire: Affaire '+self.devis),
        #     'res_model': 'stock.picking',
        #     'type': 'ir.actions.act_window',
        #     'domain': [('sale_id', '=', self.sale_ref)],
        #     # 'context': dict(self._context, create=False, editable=False),
        #     'view_mode': 'form',
        #     'views': [[form_view_id, 'form']],
        #     'flags': {'action_buttons': False},	
        #     }	

        # for data in datas:			
		# 			sale_id=data['id']
					# self.num_affaire=data['num_affaire']  
		val_id=0
		self.my_id_centralisation=self.id
		data_config = self.env['centralisation.parametrage'].search([])
		if not data_config:
			raise UserError(_("Veuillez configurer les paramètres de TVA avant de continuer!"))
		if self.state == 'draft':
			if self.nb_pending == 1:
				raise UserError(_("Veuillez centraliser la ligne en attente avant de continuer!"))
			else:
				acc_move = self.env['account.move'].sudo().create({
								'currency_id': 41,
								'ref': 'CENTRALISATION '+str(self.to_date.month).rjust(2,'0')+'/'+str(self.to_date.year),
								'date': datetime.today(),
								# 'facture_acompte': rec.facture_acompte,
								'journal_id': int(data_config.journal_tva.id),
								'company_id': 1,
								'move_type': 'entry',
								# 'financial_type': 'other',
								'id_central': self.id,
								'state': 'draft',

								'sequence_prefix': '',
								'sequence_number': 0,
								# 'name': '/',
								'narration': '<p><br></p>',
								'posted_before': False,
								'to_check': False,
								'is_move_sent': False,
								'amount_untaxed': 0,
								'amount_tax': 0,
								'amount_total': self.tva_vente,
								'amount_residual': 0,
								'amount_untaxed_signed': 0,
								'amount_tax_signed': 0,
								'amount_total_signed': self.tva_vente,
								'amount_total_in_currency_signed': self.tva_vente,
								'amount_residual_signed': 0,
								'always_tax_exigible': True,
								'auto_post': False,
								'invoice_user_id': request.env.user.id,
								'invoice_partner_display_name': '#Créé par Administrateur',

							})

				val_id=acc_move.id

				sql1="insert into account_move_line(account_id,name,debit,credit,currency_id,company_currency_id,move_id) values(%s,'TVA facturée sur vente',%s,0,41,41,%s)"  % (int(data_config.tva_vente.id),self.tva_vente,acc_move.id)
				sql2="insert into account_move_line(account_id,name,debit,credit,currency_id,company_currency_id,move_id) values(%s,'T.V.A. récupérable sur achats',0,%s,41,41,%s)"  % (data_config.tva_achat.id,self.tva_achat,acc_move.id)
				if self.tva_due > 0:
					sql3="insert into account_move_line(account_id,name,debit,credit,currency_id,company_currency_id,move_id) values(%s,'Etat, T.V.A. due',0,%s,41,41,%s)"  % (int(data_config.tva_due.id),self.tva_due,acc_move.id)
				else:
					sql3="insert into account_move_line(account_id,name,debit,credit,currency_id,company_currency_id,move_id) values(%s,'Etat, crédit de T.V.A. à reporter',%s,0,41,41,%s)"  % (int(data_config.tva_reporte.id),abs(self.tva_due),acc_move.id)
				self._cr.execute(sql1)
				self._cr.execute(sql2)
				self._cr.execute(sql3)
				self._cr.commit()

				datas = self.env['account.move'].search([('id_central', '=', self.id)])

				self.write({
					'ref_ecriture': datas.name,
					'state': 'progress'
				})

				return {
				# 'name': _('Préparation de Livraison'),
				'res_id':val_id,
				'res_model': 'account.move',
				'type': 'ir.actions.act_window',
				# 'context': "{'type':'out_invoice'}",
				# 'context': {'sale_order_id': int(self.idvente)},
				'context': {'default_id_central': self.id},
				'domain': [('journal_id', '=', int(data_config.journal_tva.id))],
				'view_mode': 'form',
				# 'target': 'new',
				'view_id': self.env.ref('account.view_move_form').id,	
				}	
		else:
			datas = self.env['account.move'].search([('id_central', '=', self.id)])
			return {
			# 'name': _('Préparation de Livraison'),
			'res_id': datas.id,
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			# 'context': "{'type':'out_invoice'}",
			# 'context': {'sale_order_id': int(self.idvente)},
			# 'context': {'default_id_central': self.id},
			'domain': [('journal_id', '=', int(data_config.journal_tva.id))],
			'view_mode': 'form',
			# 'target': 'new',
			'view_id': self.env.ref('account.view_move_form').id,	
			}	

		
	@api.onchange('from_date','to_date')
	def action_tva(self):
		# raise UserError(_("Insert Ok !!!"))
		val_due=0
		self.action_calculer_tva_vente()
		self.action_calculer_tva_achat()
		val_due = self.tva_vente - self.tva_achat
		self.tva_due = val_due


	def action_calculer_tva_vente(self):
		self.env.cr.execute("SELECT SUM(amount_tax) as tva_vente FROM account_move WHERE invoice_date between '%s' and '%s' and move_type='out_invoice' and state = 'posted'" % (self.from_date,self.to_date))
		datas = self.env.cr.dictfetchall()
		for data in datas:			
			self.tva_vente=data['tva_vente']


	def action_calculer_tva_achat(self):
		self.env.cr.execute("SELECT SUM(amount_tax) as tva_achat FROM account_move WHERE invoice_date between '%s' and '%s' and move_type='in_invoice' and state = 'posted'" % (self.from_date,self.to_date))
		datas = self.env.cr.dictfetchall()
		for data in datas:			
			self.tva_achat=data['tva_achat']


	# @api.constrains('from_date','to_date')
	# def _check_expiration_date(self):
	# 	total_lens = self.env['centralisation.tva'].search(['&',('from_date', '=', self.from_date),('to_date', '=', self.to_date)])
	# 	tot=0
	# 	for ln in total_lens:
	# 		tot +=1
	# 	total_len = self.env['centralisation.tva'].search_count(['&',('from_date', '=', self.from_date),('to_date', '=', self.to_date)])
	# 	raise ValidationError(tot)
	# 	if total_len > 0:
	# 		raise ValidationError('La centralisation de cette période a dejà été réalisée. Veuillez choisir une autre!')
	# 	# if self.from_date > self.to_date:
	# 	# 	raise ValidationError('La Date de Début doit être supérieure ou égale à la Date de Fin!')
	

	@api.depends('years')
	@api.onchange('years')
	def _calcule_nombre_annee(self):
		for rec in self:
			if rec.years==str(datetime.now().year):
				rec.nombre_annee=1
			else:
				rec.nombre_annee=0

    
	# @api.depends('months')
	@api.depends('years','months','months_now')
	@api.onchange('years','months','months_now')
	def _date_fin(self):
		if self.years==str(datetime.now().year):
			self.from_date = str(self.years)+'-'+str(self.months_now)+'-'+str(1)
			if self.months_now in ('01','03','05','07','08','10','12'):
				self.jrs_fin = 31
				self.to_date = str(self.years)+'-'+str(self.months_now)+'-'+str(self.jrs_fin)
			elif self.months_now == '02':
				if int(self.years) % 4 == 0:
					self.jrs_fin = 29
					self.to_date = str(self.years)+'-'+str(self.months_now)+'-'+str(self.jrs_fin)
				else:
					self.jrs_fin = 28
					self.to_date = str(self.years)+'-'+str(self.months_now)+'-'+str(self.jrs_fin)
			else:
				self.jrs_fin = 30
				self.to_date = str(self.years)+'-'+str(self.months_now)+'-'+str(self.jrs_fin)
		else:
			self.from_date = str(self.years)+'-'+str(self.months)+'-'+str(1)
			if self.months in ('01','03','05','07','08','10','12'):
				self.jrs_fin = 31
				self.to_date = str(self.years)+'-'+str(self.months)+'-'+str(self.jrs_fin)
			elif self.months == '02':
				if int(self.years) % 4 == 0:
					self.jrs_fin = 29
					self.to_date = str(self.years)+'-'+str(self.months)+'-'+str(self.jrs_fin)
				else:
					self.jrs_fin = 28
					self.to_date = str(self.years)+'-'+str(self.months)+'-'+str(self.jrs_fin)
			else:
				self.jrs_fin = 30
				self.to_date = str(self.years)+'-'+str(self.months)+'-'+str(self.jrs_fin)



		# total_lens = self.env['centralisation.tva'].search_count(['&',('from_date', '=', self.from_date),('to_date', '=', self.to_date)])
		# # tot=0
		# # for ln in total_lens:
		# # 	tot +=1
		# # total_len = self.env['centralisation.tva'].search_count(['&',('from_date', '=', self.from_date),('to_date', '=', self.to_date)])
		# # raise ValidationError(total_lens)
		# if total_lens > 0:
		# 	raise ValidationError('La centralisation de cette période a dejà été réalisée. Veuillez choisir une autre!')


	def _conct_date(self):
		for rec in self:
			rec.conct_date = str(rec.years)+'/'+str(rec.months)+'/'+str(rec.jrs_fin)


	# def _from_date(self):
	# 	for rec in self:
	# 		# rec.from_date = date(int(rec.years), int(rec.months), day=1)
	# 		rec.from_date = str(rec.years)+'-'+str(rec.months)+'-'+str('01')

	# def _to_date(self):
	# 	for rec in self:
	# 		# rec.to_date = date(int(rec.years), int(rec.months), int(rec.jrs_fin))
	# 		rec.to_date = str(rec.years)+'-'+str(rec.months)+'-'+str(rec.jrs_fin)


	# @api.multi
	def unlink(self):
		for record in self:
			if record.state != 'draft':
				raise UserError(_('Vous ne pouvez pas supprimer une ligne de centralisation en cours de traitement ou publiée!'))
		return super(CentralisationTva, self).unlink()



	# def unlink(self):
    #     # res = super(AccountMoveCustoms, self).unlink()
    #     if self.state =='draft':
    #         sql1="update centralisation_tva set ref_ecriture='%s',state='draft' where id=%d"  % ('',self.id_central)
    #         self._cr.execute(sql1)
    #         self._cr.commit()

    #     res = super(AccountMoveCustoms, self).unlink()

    #     # tree_view_id = self.env.ref('madata_custom.centralisation_tva_tree').ids
    #     # form_view_id = self.env.ref('stock.view_picking_form').ids   
    #     return res #super(AccountMoveCustoms, self).unlink()

	# @api.ondelete(at_uninstall=False)
	# def _unlink_except_tva(self):
	# 	# Prevent deleting lines on posted entries
	# 	for rec in self:
	# 		if not self._context.get('force_delete') and any(m.state == 'progress' or m.state == 'done'  for m in (rec.id,rec.id)):
	# 			raise UserError(_('Vous ne pouvez pas supprimer une ligne de centralisation en cours de traitement ou publiée!'))


class CentralisationParametrage(models.Model):
    _name = "centralisation.parametrage"
    # _rec_name = 'years'

    tva_vente= fields.Many2one("account.account", string='Tva sur vente',required=True)
    tva_achat= fields.Many2one("account.account", string='Tva sur achat',required=True)
    tva_due= fields.Many2one("account.account", string='Tva due',required=True)
    tva_reporte= fields.Many2one("account.account", string='Tva reporter',required=True)
    journal_tva= fields.Many2one("account.journal", string='Journal tva',required=True)

