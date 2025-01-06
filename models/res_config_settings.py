from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_auto_reminders = fields.Boolean(
        string='Enable Automatic Reminders',
        config_parameter='custom_crm.enable_auto_reminders',
        default=True
    )
