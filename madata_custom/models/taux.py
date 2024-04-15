from odoo import models, fields, api, _

class TauxConfiguration(models.Model):
    _name = "taux.configuration.vente"
    _description='Taux Frais Généraux'
    _rec_name = 'taux'

    taux = fields.Float(string='Taux Configuration Frais Généraux')
