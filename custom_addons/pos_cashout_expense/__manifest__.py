# -*- coding: utf-8 -*-
{
    'name': 'POS Cashout to Expense',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Create expense records from POS cash out transactions',
    'description': """
POS Cashout to Expense Integration
===================================
This module extends the POS Cash In/Out functionality to allow creating
expense records directly from cash out transactions.

Features:
---------
* Add "Add to Expense" button in Cash Out popup
* Automatically create hr.expense records from cash out transactions
* Link expenses to bank statement lines for traceability
* Only available for cash out (not cash in) transactions
    """,
    'author': 'PetSpot',
    'website': '',
    'depends': [
        'point_of_sale',
        'hr_expense',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_cashout_expense/static/src/js/cash_move_popup.js',
            'pos_cashout_expense/static/src/xml/cash_move_popup.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

