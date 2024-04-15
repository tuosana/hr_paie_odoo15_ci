# -*- coding: utf-8 -*-

from odoo import api, fields, _, models, exceptions
from odoo.exceptions import AccessError,UserError

class HrContractEmployee(models.Model):
    _inherit = "hr.contract"

    # les fontion d'impression
    def print_certificat_travail(self):

        if not self.date_end: raise UserError(_("Veuillez remplir la Date de fin du contrat"))        
        return self.env.ref('madata_custom.report_certificat_trav').report_action(self)


    def print_attestation_travail(self):
        if not self.job_id: raise UserError(_("Veuillez remplir le poste occupé par l'employé!"))  
        return self.env.ref('madata_custom.report_attestation_travail').report_action(self)
        