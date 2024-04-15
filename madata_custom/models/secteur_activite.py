# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError

class SecteurActivite(models.Model):
    _name = 'secteur.activite'
    _description='Secteur Activite'
    # _rec_name = 'designation_preparation'

    name = fields.Char(string='Secteur Activité')


class ActiviteEntreprise(models.Model):
    _name = 'activite.entreprise'
    _description='Activite'
    # _rec_name = 'designation_preparation'

    name = fields.Char(string='Activité')
    nametest = fields.Char(string='Activité')
    secteur_act = fields.Many2one('secteur.activite', string='Secteur Activité',)


class CategorieSociete(models.Model):
    _name = 'categorie.societe'
    _description='Catégorie Societé'
    # _rec_name = 'designation_preparation'

    name = fields.Char(string='Catégorie Societé')
    # secteur_act = fields.Many2one('secteur.activite', 'Secteur Activité',)


# class CategorieSociete(models.Model):
#     _inherit = 'res.partner'
#     _description='Contact Partenaire'
#     # _rec_name = 'designation_preparation'

#     namecc = fields.Char(string='Catégorie Societé')
#     namecc1 = fields.Char(string='Catégorie Societé 1')
    # categ_societe = fields.Many2one('categorie.societe', string='Catégorie Société',)
    # secteur_act = fields.Many2one('secteur.activite', 'Secteur Activité',)


# class ContactClientFormInherit(models.Model):
#     _inherit = 'res.partner'

#     # categ_societe = fields.Many2one('categorie.societe', string='Catégorie Société',)
# 	# secteur_acts = fields.Many2one('secteur.activite', string='Secteur Activité',)
# 	# secteur_a_ts = fields.One2many('secteur.activite', 'secteur_acts',)
# 	# activite_ent = fields.Many2one('activite.entreprise', 'Activité Entreprise',)
#     nbemp = fields.Integer(string='Nombre Employé')
