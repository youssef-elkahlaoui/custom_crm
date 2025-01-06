from odoo import models, fields, api

class CrmOpportunity(models.Model):
    _inherit = 'crm.lead'

    # Champs additionnels si nécessaire
    # ...

    @api.model
    def _cron_archive_opportunities(self):
        thirty_days_ago = fields.Date.today() - fields.Date.delta(days=30)
        opportunities = self.search([('create_date', '<', thirty_days_ago), ('active', '=', True)])
        opportunities.action_archive()