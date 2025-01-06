from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _get_portal_return_action(self):
        """ Custom method for portal return action """
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Opportunities',
            'view_mode': 'kanban,form',
            'res_model': 'crm.lead',
            'domain': [('partner_id.user_ids', 'in', self.env.user.ids)]
        }