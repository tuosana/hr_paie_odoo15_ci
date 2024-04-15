# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError


class CategorieSociete(models.Model):
    _name = 'categorie.societe'
    _description='Catégorie Societé'
    # _rec_name = 'designation_preparation'

    name = fields.Char(string='Catégorie Societé')
    # secteur_act = fields.Many2one('secteur.activite', 'Secteur Activité',)
