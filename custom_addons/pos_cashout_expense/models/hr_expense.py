# -*- coding: utf-8 -*-

from odoo import fields, models


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    pos_statement_line_id = fields.Many2one(
        'account.bank.statement.line',
        string='POS Statement Line',
        help='Bank statement line linked to this expense from POS cash out',
        readonly=True,
        copy=False,
    )
    pos_session_id = fields.Many2one(
        'pos.session',
        string='POS Session',
        related='pos_statement_line_id.pos_session_id',
        store=True,
        readonly=True,
        help='POS Session from which this expense was created',
    )

