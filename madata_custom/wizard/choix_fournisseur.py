# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError,AccessError


class ListeFournisseur(models.TransientModel):
    _name='choix.fournisseur'
    # _description='Choix Fournisseur'
    
    # product_id= fields.Integer(string='Produit',)
    product_id = fields.One2many('product.supplierinfo', 'product_tmpl_id',)
    supplier_id = fields.Many2one('res.partner', string='Client',)
    price= fields.Integer(string='Prix',)
    delay= fields.Integer(string='Délai Livraison',) 

    # def init(self,p):
    # def init(self):
    #     self._cr.execute("""
    #         CREATE OR REPLACE VIEW choix_fournisseur AS (
    #             SELECT row_number() OVER () as id,
    #             name as supplier_id,
    #             price,
    #             delay
    #             FROM product_supplierinfo
    #             WHERE
    #             product_tmpl_id=5
    #             ORDER BY price,delay
    #         )""")
    #         # )""",(p))

    def action_confirm(self):
        active_ids = self._context.get('active_ids')
       
    #     data= {
    #         'form_data': self.read()[0],
    #         'donnees': self._get_lines(self.date_from,self.date_to,self.commune.id)
    #     }
    #     # print (self._get_lines(self.date_from,self.date_to,int(self.commune.id)))
    #     return self.env.ref('dce_dgi.action_report_dgi').with_context(landscape=True).report_action(self, data=data)


   