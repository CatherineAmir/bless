# -*- coding: utf-8 -*-
{
    'name': "bless",

    'summary': """
        Database for Bless Service
        """,

    'description': """
       
    """,

    'author': "Sita Egypt",
    'website': "http://www.sita-eg.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/regions_views.xml',
        'views/servants_view.xml',
        'views/occasions_views.xml',
        'views/units_views.xml',
        'views/family_view.xml',
        'views/food_beverage_views.xml',
        'views/concrete_views.xml',
        'views/members_view.xml',
        'views/giving.xml',
        'wizards/create_giving_wizard.xml',
        'reports/report.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
