from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'opportunity_count' in counters:
            opportunity_count = request.env['crm.lead'].search_count([
                ('partner_id.user_ids', 'in', [request.env.user.id])
            ]) if request.env.user.has_group('base.group_portal') else 0
            values['opportunity_count'] = opportunity_count
        return values

    @http.route(['/my/opportunities', '/my/opportunities/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_opportunities(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmLead = request.env['crm.lead']

        domain = [
            ('partner_id.user_ids', 'in', [request.env.user.id])
        ]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # count for pager
        opportunity_count = CrmLead.search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/opportunities",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=opportunity_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        opportunities = CrmLead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'opportunities': opportunities,
            'page_name': 'opportunities',
            'pager': pager,
            'default_url': '/my/opportunities',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("custom_crm.portal_my_opportunities", values)
