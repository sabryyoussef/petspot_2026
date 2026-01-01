# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PosSession(models.Model):
    _inherit = 'pos.session'

    def prepare_expense_from_cashout(self, statement_line_id, amount, reason, partner_id):
        """
        Prepare (create draft) an hr.expense record from a cash out transaction
        and return the action to open it in form view
        
        Args:
            statement_line_id: ID of account.bank.statement.line
            amount: Cash out amount (positive value)
            reason: Reason/description from cash out
            partner_id: Partner ID (employee)
        
        Returns:
            Action dict to open expense form view
        """
        self.ensure_one()
        
        # Verify statement line belongs to this session
        statement_line = self.env['account.bank.statement.line'].browse(statement_line_id)
        if statement_line.pos_session_id != self:
            raise UserError(_("The statement line does not belong to this POS session."))
        
        # Verify it's a cash out (negative amount)
        if statement_line.amount >= 0:
            raise UserError(_("Only cash out transactions can be converted to expenses."))
        
        # Get employee from partner
        employee = self.env['hr.employee'].search([
            ('user_id.partner_id', '=', partner_id)
        ], limit=1)
        
        if not employee:
            # Try to get employee from current user
            employee = self.env.user.employee_id
            if not employee:
                raise ValidationError(_('No employee found for this user. Please create an employee record.'))
        
        # Get default expense product (first expensable product)
        expense_product = self.env['product.product'].search([
            ('can_be_expensed', '=', True)
        ], limit=1)
        
        if not expense_product:
            raise UserError(_("No expense product found. Please configure at least one product with 'Can be Expensed' enabled."))
        
        # Prepare expense values
        # In Odoo 19, expenses use total_amount_currency which is computed from quantity * price_unit
        expense_vals = {
            'name': reason or _('Cash Out from POS'),
            'employee_id': employee.id,
            'product_id': expense_product.id,
            'quantity': 1.0,
            'total_amount_currency': abs(amount),  # Set total amount - Odoo 19 will compute price_unit
            'date': statement_line.date or fields.Date.context_today(self),
            'description': _('Cash out from POS Session: %s\nReason: %s') % (self.name, reason or ''),
            'payment_mode': 'own_account',
            'company_id': self.company_id.id,
            'pos_statement_line_id': statement_line_id,  # Link to statement line
            'state': 'draft',  # Create as draft so user can edit
        }
        
        # Create expense as draft
        expense = self.env['hr.expense'].create(expense_vals)
        
        # Return expense ID and action ID for opening form
        # Get the action to open expense form view
        try:
            action = self.env['ir.actions.act_window']._for_xml_id('hr_expense.hr_expense_action_my_all')
            action_id = action.get('id')
        except:
            # Fallback if action not found
            action_id = None
        
        return {
            'expense_id': expense.id,
            'expense_name': expense.name,
            'action_id': action_id,
        }

