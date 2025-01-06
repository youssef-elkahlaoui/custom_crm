from odoo import models, fields

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    is_feedback_survey = fields.Boolean(string='Est un questionnaire de feedback', default=False)
