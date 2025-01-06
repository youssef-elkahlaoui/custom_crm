from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    opportunity_count = fields.Integer(compute='_compute_opportunity_count', string='Opportunity Count')
    
    def _compute_opportunity_count(self):
        for partner in self:
            partner.opportunity_count = self.env['crm.lead'].search_count([
                ('partner_id', '=', partner.id),
                ('type', '=', 'opportunity')
            ])
