from odoo import http
from odoo.http import request

class FeedbackController(http.Controller):

    @http.route('/crm/feedback/<int:activity_id>', type='http', auth='user', website=True)
    def feedback_form(self, activity_id, **kwargs):
        activity = request.env['mail.activity'].sudo().browse(activity_id)
        # Logique pour afficher le formulaire de feedback
        # ...
        return request.render('custom_crm.feedback_template', {'activity': activity})