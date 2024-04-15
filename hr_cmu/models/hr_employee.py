# -*- coding:utf-8 -*-


from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    pay_for_women=fields.Selection([('yes', 'Oui'),('no', 'Non')], "Payé Part CMU de son époux(se)", default='yes')
    cmu_part = fields.Integer("Nombre de perssones à prendre en compte pour la CMU",
                              compute= "_compute_part_cmu", store=True)

    # @api.depends("enfants_ids")
    # def _compute_part_cmu(self):
    #     for emp in self:
    #         part_cmu = emp.children + 1
    #         if emp.marital == 'married':
    #             part_cmu += 1
    #         emp.cmu_part = part_cmu
    
    @api.depends("enfants_a_charge","enfants_ids","pay_for_women","marital")
    @api.onchange("enfants_a_charge","enfants_ids","pay_for_women","marital")
    def _compute_part_cmu(self):
        for emp in self:
            if emp.pay_for_women == 'yes':
                part_cmu = emp.enfants_a_charge + 1
                if emp.marital == 'married':
                    part_cmu += 1
                emp.cmu_part = part_cmu
            else:
                part_cmu = emp.enfants_a_charge + 1
                # if emp.marital == 'married':
                # part_cmu += 1
                emp.cmu_part = part_cmu

    # cmu_part = fields.Integer("Nombre de perssones à prendre en compte pour la CMU",
    #                           compute= "_compute_part_cmu", store=False)

