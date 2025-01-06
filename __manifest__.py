{
    'name': 'CRM Avancé',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Fonctionnalités avancées pour la gestion des opportunités',
    'description': """
        Module CRM personnalisé avec:
        - Tableaux de bord personnalisés par rôle
        - Gestion des accès et sécurité
        - Vue portail client
    """,
    'depends': [
        'base',
        'crm',
        'mail',
        'portal',
        'sales_team',
        'contacts',
    ],
    'data': [
        'security/crm_security.xml',
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
        'wizards/crm_lost_reason_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}