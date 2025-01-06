from odoo import models, fields, api
from datetime import datetime, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    feedback_survey_id = fields.Many2one('survey.survey', string='Questionnaire Feedback')

    client_rating = fields.Selection(
        related='partner_id.client_rating',
        string='Note Client',
        readonly=True
    )
    last_followup_date = fields.Datetime('Dernier suivi')
    next_followup_date = fields.Datetime('Prochain suivi', compute='_compute_next_followup')
    feedback_submitted = fields.Boolean('Feedback soumis', default=False)
    feedback_score = fields.Float('Score Feedback', default=0.0)
    lost_reason_detailed = fields.Selection([
        ('price', 'Prix trop élevé'),
        ('communication', 'Manque de communication'),
        ('product', 'Produit inadapté')
    ], string='Raison détaillée de la perte')
    lost_price_difference = fields.Float('Différence de prix (%)')

    @api.depends('last_followup_date')
    def _compute_next_followup(self):
        for lead in self:
            if lead.last_followup_date:
                lead.next_followup_date = fields.Datetime.from_string(lead.last_followup_date) + timedelta(days=1)
            else:
                lead.next_followup_date = fields.Datetime.now() + timedelta(days=1)

    def action_set_lost(self):
        return {
            'name': 'Raison de la perte',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lost.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lead_id': self.id}
        }

    def mark_followup_done(self):
        self.write({
            'last_followup_date': fields.Datetime.now()
        })

    @api.model
    def _cron_opportunity_reminder(self):
        opportunities = self.search([
            ('type', '=', 'opportunity'),
            ('stage_id.is_won', '=', False),
            ('next_followup_date', '<=', fields.Datetime.now()),
            ('active', '=', True)
        ])
        template = self.env.ref('custom_crm.email_template_opportunity_reminder')
        for opp in opportunities:
            template.send_mail(opp.id, force_send=True)

    def action_mark_won(self):
        res = super(CrmLead, self).action_mark_won()
        template = self.env.ref('custom_crm.email_template_opportunity_won')
        for lead in self:
            template.send_mail(lead.id, force_send=True)
        return res