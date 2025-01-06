{
    'name': 'Custom CRM',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Custom CRM features with client portal',
    'description': """
        Custom CRM module with enhanced features:
        * Client portal access to opportunities
        * Custom dashboards for different user roles
        * Enhanced opportunity management
    """,
    'depends': [
        'base',
        'crm',
        'portal',
        'website',
        'sales_team',
    ],
    'data': [
        'security/crm_security.xml',
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}