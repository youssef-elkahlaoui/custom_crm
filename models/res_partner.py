from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    client_type = fields.Selection([
        ('retail', 'Client Retail'),
        ('wholesale', 'Client Grossiste'),
        ('distributor', 'Distributeur')
    ], string='Type de client', default='retail')

    total_purchases = fields.Integer(
        string='Nombre d\'achats',
        compute='_compute_total_purchases',
        store=True
    )

    client_rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], string='Note client', compute='_compute_client_rating', store=True)

    contact_method = fields.Selection([
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('mail', 'Courrier postal')
    ], string='Méthode de contact préférée', default='email')

    last_contact = fields.Date(string='Dernière date de contact')
    next_contact = fields.Date(string='Prochaine date de contact')
    client_notes = fields.Text(string='Notes internes')

    @api.depends('sale_order_ids')
    def _compute_total_purchases(self):
        for partner in self:
            partner.total_purchases = len(partner.sale_order_ids.filtered(lambda o: o.state == 'sale'))

    @api.depends('total_purchases')
    def _compute_client_rating(self):
        for partner in self:
            if partner.total_purchases >= 20:
                partner.client_rating = '5'
            elif partner.total_purchases >= 15:
                partner.client_rating = '4'
            elif partner.total_purchases >= 10:
                partner.client_rating = '3'
            elif partner.total_purchases >= 5:
                partner.client_rating = '2'
            else:
                partner.client_rating = '1'
