from odoo import models, fields, api

class CrmLostReasonWizard(models.TransientModel):
    _name = 'crm.lost.reason.wizard'
    _description = 'Raison détaillée de la perte de l\'opportunité'

    lead_id = fields.Many2one('crm.lead', string='Opportunité')
    lost_reason = fields.Selection([
        ('price', 'Prix trop élevé'),
        ('communication', 'Manque de communication'),
        ('product', 'Produit inadapté')
    ], string='Raison de la perte', required=True)
    price_difference = fields.Float('Différence de prix (%)', help="Différence en pourcentage avec le prix concurrent")
    notes = fields.Text('Notes supplémentaires')

    def action_confirm_lost(self):
        self.ensure_one()
        self.lead_id.write({
            'lost_reason_detailed': self.lost_reason,
            'lost_price_difference': self.price_difference if self.lost_reason == 'price' else 0,
            'active': False,
        })
        return {'type': 'ir.actions.act_window_close'}
