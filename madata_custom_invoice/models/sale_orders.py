# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date

class sale_order(models.Model):
    _inherit = 'sale.order'

    date_du_devis = fields.Datetime(string="Date du devis")

    #THINK GOOD
    @api.model
    def create(self, values):
        """
            Create a new record for a model sale_subscription
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
    
        result = super(sale_order, self).create(values)

        opportunities_domain = [('id','=',result.opportunity_id.id),]
        all_opportunities = self.env['crm.lead'].search(opportunities_domain, order='id desc')

        if len(all_opportunities) > 0:
            result.opportunity_id.write({
                'expected_revenue': result.amount_untaxed
            })
            # if result.opportunity_id.society:
            #     result.write({
            #         'team_id': result.opportunity_id.team_id.id,
            #         # 'society': result.opportunity_id.society
            #     })

        # sequence_devis = self.env['ir.sequence'].next_by_code('adisa.sale.order')
        # now = datetime.now()
        # today = now.date()
        # la_date = today.strftime("%y/%m/%d")
        # numero_devis = str(la_date) + '/' + str(sequence_devis)

        # result.write({
        #     'name': numero_devis,
        #     #'date_order': result.date_du_devis
        # })

        return result

    
    #@api.multi
    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise
    
            @param values: dict of new values to be set
    
            @return: True on success, False otherwise
        """
        result = super(sale_order, self).write(values)

        for any_rec in self:
            # opportunities_domain = [('id','=',any_rec.opportunity_id.id),]
            # all_opportunities = self.env['crm.lead'].search(opportunities_domain, order='id desc')

            order_domain = [('opportunity_id','=',any_rec.opportunity_id.id),]
            all_order = self.env['sale.order'].search(order_domain, order='id desc')

            if any_rec.id == all_order[0].id:
                all_order[0].opportunity_id.write({
                    'expected_revenue': all_order[0].amount_untaxed
                })

            # self.write({
            #     'team_id': self.opportunity_id.team_id.id,
            #     'society': self.opportunity_id.society
            # })
        # if self.opportunity_id.society:   
        #     self.write({
        #         'society': self.opportunity_id.society
        #     })
    
        return result