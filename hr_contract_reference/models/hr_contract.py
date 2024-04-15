# copyright 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class HrContract(models.Model):
    _inherit = "hr.contract"

    name = fields.Char("Contract Reference", required=False, readonly=True, copy=False, default="/")

    @api.model
    def create(self, vals):
        if vals.get("name", "/") == "/":
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code("contract.ref") or _('N/A')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code("contract.ref") or _('N/A')
        print(vals['name'])
        return super(HrContract, self).create(vals)
