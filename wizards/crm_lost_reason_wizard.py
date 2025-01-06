from odoo import models, fields

class CrmLostReasonWizard(models.TransientModel):
    _name = 'crm.lost.reason.wizard'
    _description = 'Lost Reason Wizard'

    lost_reason_id = fields.Many2one('crm.lost.reason', string='Lost Reason')
    lead_id = fields.Many2one('crm.lead', string='Opportunity')

    def action_lost_reason_apply(self):
        self.ensure_one()
        self.lead_id.write({
            'lost_reason': self.lost_reason_id.id,
            'active': False,
        })
        return {'type': 'ir.actions.act_window_close'}
