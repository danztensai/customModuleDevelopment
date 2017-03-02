# -*- coding: utf-8 -*-
{
    'name': "custom Quotation",

    'summary': """
        Custom Quotation""",

    'description': """
Add New field :
destinasi
delivery order
Vehicle type
Vechile number
    """,

    'author': "Danial Habibi",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
