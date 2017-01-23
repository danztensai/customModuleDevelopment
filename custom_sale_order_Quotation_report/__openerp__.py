# -*- coding: utf-8 -*-
{
    'name': "Custom Sale Order Report Quotation",

    'summary': """
        Add Few Field To report""",

    'description': """
Field Report Tambahkan Truck Number
Field Report Tambahkan Deliver date
Field Report Tambahkan Delivery order Number
Field Report Tambahkan Destination
Field Report Tambahkan Truck Type

    """,

    'author': "Danial Habibi",
    'website': "-",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.1',

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
