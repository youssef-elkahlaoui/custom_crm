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
        ('product', 'Produit inadapté'),
        ('competition', 'Concurrence'),
        ('timing', 'Mauvais timing'),
        ('features', 'Fonctionnalités manquantes'),
        ('other', 'Autre')
    ], string='Raison détaillée de la perte')
    lost_price_difference = fields.Float('Différence de prix (%)')
    archive_date = fields.Datetime('Date d\'archivage')
    reminder_count = fields.Integer('Nombre de rappels', default=0)
    last_reminder_sent = fields.Datetime('Dernier rappel envoyé')
    requires_manager_attention = fields.Boolean('Attention manager requise', default=False)

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

    def notify_sales_person(self):
        """Send reminder to sales person"""
        if self.user_id:
            self.env['mail.message'].create({
                'model': 'crm.lead',
                'res_id': self.id,
                'message_type': 'notification',
                'partner_ids': [(4, self.user_id.partner_id.id)],
                'subject': 'Rappel: Suivi d\'opportunité nécessaire',
                'body': f'L\'opportunité {self.name} nécessite votre attention.'
            })
            self.reminder_count += 1
            self.last_reminder_sent = fields.Datetime.now()

    def notify_manager(self):
        """Notify manager for won opportunities"""
        if self.team_id and self.team_id.user_id:
            self.env['mail.message'].create({
                'model': 'crm.lead',
                'res_id': self.id,
                'message_type': 'notification',
                'partner_ids': [(4, self.team_id.user_id.partner_id.id)],
                'subject': 'Nouvelle opportunité gagnée',
                'body': f'L\'opportunité {self.name} a été gagnée. Veuillez créer un bon de commande.'
            })
            self.requires_manager_attention = True

    @api.model
    def _cron_auto_archive_opportunities(self):
        """Auto archive opportunities after 30 days without feedback"""
        deadline = fields.Datetime.now() - timedelta(days=30)
        opportunities = self.search([
            ('type', '=', 'opportunity'),
            ('feedback_submitted', '=', False),
            ('create_date', '<', deadline),
            ('active', '=', True)
        ])
        for opp in opportunities:
            opp.write({
                'active': False,
                'archive_date': fields.Datetime.now()
            })
            # Send final notification
            opp.notify_sales_person()
            if opp.partner_id and opp.partner_id.email:
                template = self.env.ref('custom_crm.email_template_opportunity_archived')
                template.send_mail(opp.id)

    @api.model
    def _cron_send_reminders(self):
        """Send reminders at different intervals"""
        intervals = [
            (1, 'Rappel 24h'),
            (2, 'Rappel 48h'),
            (3, 'Rappel 72h'),
            (7, 'Rappel 1 semaine')
        ]
        
        for days, reminder_type in intervals:
            deadline = fields.Datetime.now() - timedelta(days=days)
            opportunities = self.search([
                ('type', '=', 'opportunity'),
                ('feedback_submitted', '=', False),
                ('create_date', '<', deadline),
                ('reminder_count', '=', days - 1)
            ])
            for opp in opportunities:
                opp.notify_sales_person()

    def action_set_won(self):
        """Override to add manager notification"""
        res = super(CrmLead, self).action_set_won()
        self.notify_manager()
        return res

    def get_opportunity_analytics(self):
        """Get analytics for lost opportunities"""
        domain = [
            ('type', '=', 'opportunity'),
            ('stage_id.is_won', '=', False),
            ('lost_reason_detailed', '!=', False)
        ]
        opportunities = self.search(domain)
        
        analytics = {}
        for reason in dict(self._fields['lost_reason_detailed'].selection):
            analytics[reason] = len(opportunities.filtered(lambda o: o.lost_reason_detailed == reason))
        
        return analytics