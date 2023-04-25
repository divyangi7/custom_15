# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': '',
    'description': """

    """,
    'depends': ['mail','sale'],
    'data': [
        'security/ir.model.access.csv',
        'Data/cron.xml',
        'wizard/property_wizard_views.xml',
        'views/real_estate_views.xml',
        'views/property_type_views.xml',
        'views/property_tag_views.xml',
        'views/property_offer_views.xml',
        'views/res_users.xml',
        'security/security.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'views/res_config_settings_views.xml'

    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {}
}
