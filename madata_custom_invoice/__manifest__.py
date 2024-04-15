# -*- coding: utf-8 -*-
{
    'name': "MADATA CUSTOM INVOICES",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Environnent de travail MADATA
    """,

    'author': "My Company",
    'website': "adisa.digital",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ERP DE MADATA',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','analytic', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_custom_view.xml',
        # 'views/hr_payslip_custom_view.xml',
        # 'views/hr_expense_custom_view.xml',
        # 'views/hr_expense_request.xml',
        # 'views/sale_order.xml',
        # 'report/report_piece_caisse.xml',
        # 'wizard/hr_expense_report_wizard_view.xml',
        # 'wizard/expense_sheet_wizard.xml', 
        # 'wizard/expense_sheet_wizard1.xml',
        # 'wizard/report_hr_expense_wizard1.xml',  
        # 'views/login.xml',
        'views/website_templates.xml',
	    'views/account_move_view.xml',
        #'views/hr_contract_view.xml', 
        # 'views/account_bank_statement_view.xml',
        # 'security/security.xml',
        # 'report/report_invoice_custom.xml',
        'report/invoice.xml',
        'report/invoice_no_header_with_payment.xml',
        'report/invoice_no_header.xml',
        'report/livraison_bon_document.xml',
        'report/livraison_bon.xml',
        # 'report/report_bon_livraison.xml',
        'report/report_menu.xml',
        'report/report_menu_payment.xml',
    ],
    # 'assets': {'web.assets_backend': ['madata_custom_invoice/static/src/js/menu.js']},
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml', 
    ],

    # 'assets': {
    #     'web.assets_frontend': [
    #         'static/src/css/custom_invoice.css',
    #     ]
    # }
}
