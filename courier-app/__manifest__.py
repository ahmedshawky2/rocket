# -*- coding: utf-8 -*-
{
    'name': "courier-app",

    'summary': """
        Extend Sales Module to be as Courier Services Module""",

    'description': """
        Developed By Minds Solutions
    """,

    'author': "Minds Solutions",
    'website': "http://www.mindseg.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/product_view.xml',
        #'views/my_website.xml',
        'views/my_views.xml',
        'data/invoice_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}