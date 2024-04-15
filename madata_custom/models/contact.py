# -*- coding: utf-8 -*-

from odoo import api, fields, _, models
from odoo.exceptions import AccessError,UserError,ValidationError
# from datetime import datetime


class ContactPartenaire(models.Model):
	_inherit = 'res.partner'
	# _name = "contact.partenaire"
	
	code_ref = fields.Char(string='Code',)
	code_cc = fields.Char(string='Numéro CC',)
	categ_societe = fields.Many2one('categorie.societe', string='Catégorie Société',)
	secteur_acts = fields.Many2one('secteur.activite', string='Secteur Activité',)
	activite_ent = fields.Many2one('activite.entreprise', string='Activité Entreprise',)
	type_f = fields.Selection([('local','Local'), ('etranger','Etranger')],'Type', default='local')
	nbemp = fields.Integer(string='Nombre Employé(s)')
	# type_f = fields.Selection([('local','Local'), ('etranger','Etranger')],'Type fournisseur', default="local")

	# nc_contribuable= fields.Char(string='N. C. Contribuable', store=True)
	nc_client= fields.Char(string='N. C. Client', store=True)
