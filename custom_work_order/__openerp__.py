{
    'name': "Custom Work Order",

    'summary': """
        Custom Work Order with custom field""",

    'description': """
Add New field :
Route \n
Loading PLAN \n 
Arrival PLAN \n
SPM \n 
Start Loading
Finish Loading
Loading Doc Finish
Distpach From Origin
Actual Arrival Time
Start Unloading
Finish Unloading
Finish DOC Loading
Depart From Destination
STATUS
Remark
    """,

    'author': "Danial Habibi",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet_work_order','fleet_work_order_multiple_route'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml','report.xml','report_delivery_note.xml','data/master_data_company.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
