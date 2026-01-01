/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { CashMoveReceipt } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_receipt/cash_move_receipt";
import { _t } from "@web/core/l10n/translation";

patch(CashMovePopup.prototype, {
    setup() {
        super.setup(...arguments);
        // Track the last created statement line ID for expense creation
        // Add to reactive state so template updates automatically
        this.lastStatementLineId = null;
        this.lastCashOutAmount = null;
        this.cashOutConfirmed = false;  // Track if cashout was confirmed
        
        // Add reactive properties to state object for template reactivity
        // useState makes state reactive, so changes will update the template automatically
        if (this.state) {
            this.state.cashOutConfirmed = false;
            this.state.lastStatementLineId = null;
        }
    },

    async confirm() {
        // Store amount and reason before calling super
        const amount = parseFloat(this.state.amount);
        const reason = this.state.reason.trim();
        const type = this.state.type;
        const wasCashOut = type === 'out' && amount > 0;
        
        // For cash out, handle it manually to keep popup open for "Add to Expense" button
        if (wasCashOut) {
            const formattedAmount = this.env.utils.formatCurrency(amount);
            const translatedType = _t('out');
            const extras = { formattedAmount, translatedType };
            
            // Call backend to create cash out
            await this.pos.data.call(
                "pos.session",
                "try_cash_in_out",
                this._prepareTryCashInOutPayload(type, amount, reason, this.partnerId, extras),
                {},
                true
            );
            
            // Log employee message
            await this.pos.logEmployeeMessage(
                `${_t("Cash")} ${translatedType} - ${_t("Amount")}: ${formattedAmount}`,
                "CASH_DRAWER_ACTION"
            );
            
            // Print receipt (same as original)
            // Access via pos store getters (session, company, user are getters on pos store)
            const order = this.pos.models["pos.order"].create({
                session_id: this.pos.session.id,
                company_id: this.pos.company,
                config_id: this.pos.config.id,
                user_id: this.pos.user.id,
                ticket_code: "",
                tracking_number: "",
                sequence_number: 0,
                pos_reference: "",
            });
            await this.printer.print(CashMoveReceipt, {
                reason,
                translatedType,
                order: order,
                formattedAmount,
                date: new Date().toLocaleString(),
            });
            this.pos.models["pos.order"].delete(order);
            
            // Get statement line ID first (before marking as confirmed)
            await new Promise(resolve => setTimeout(resolve, 300));
            
            const cashMoves = await this.pos.data.call(
                "pos.session",
                "get_cash_in_out_list",
                [this.pos.session.id]
            );
            
            let statementLineId = null;
            if (cashMoves && cashMoves.length > 0) {
                const latestMove = cashMoves[cashMoves.length - 1];
                if (latestMove.amount < 0 && Math.abs(latestMove.amount) === amount) {
                    statementLineId = latestMove.id;
                }
            }
            
            // Mark cashout as confirmed and set statement line ID
            this.lastCashOutAmount = amount;
            
            // Update reactive state - this will trigger template update automatically
            if (this.state) {
                this.state.cashOutConfirmed = true;
                this.state.lastStatementLineId = statementLineId;
            }
            
            // Show success message but DON'T close popup - keep it open
            this.notification.add(
                _t("Cash out confirmed. Click 'Add to Expense' to create expense."),
                { type: 'success' }
            );
            
            // Don't close popup - return so it stays open with "Add to Expense" button enabled
            return;
        }
        
        // For cash in, use original behavior (closes popup)
        await super.confirm(...arguments);
    },

    async openExpenseForm() {
        if (this.state.type !== 'out') {
            this.notification.add(_t("Expenses can only be created from cash out transactions."), {
                type: 'warning',
            });
            return;
        }

        const amount = parseFloat(this.state.amount);
        if (!amount || amount <= 0) {
            this.notification.add(_t("Please enter a valid cash out amount."), {
                type: 'warning',
            });
            return;
        }

        // Ensure cashout is confirmed first
        const confirmed = this.state?.cashOutConfirmed || false;
        const statementLineId = this.state?.lastStatementLineId || null;
        
        if (!confirmed || !statementLineId) {
            this.notification.add(
                _t("Please confirm the cash out first before adding to expense."),
                { type: 'warning' }
            );
            return;
        }

        const reason = this.state.reason.trim() || _t('Cash Out from POS');

        try {
            // Prepare expense and get expense ID
            const result = await this.pos.data.call(
                "pos.session",
                "prepare_expense_from_cashout",
                [
                    this.pos.session.id,
                    statementLineId,
                    amount,
                    reason,
                    this.partnerId,
                ],
                {},
                true
            );

            // Build the URL to open the expense form in backend
            // Get base URL - try different methods
            let baseUrl = this.pos.config._base_url;
            if (!baseUrl) {
                // Fallback to current location
                const currentUrl = window.location.href;
                const urlObj = new URL(currentUrl);
                baseUrl = `${urlObj.protocol}//${urlObj.host}`;
            }
            
            // Odoo URL format: /web#id=<record_id>&model=<model_name>&view_type=form
            // If action_id is provided, use it in the URL
            let expenseUrl;
            if (result.action_id) {
                expenseUrl = `${baseUrl}/web#id=${result.expense_id}&model=hr.expense&view_type=form&action=${result.action_id}`;
            } else {
                expenseUrl = `${baseUrl}/web#id=${result.expense_id}&model=hr.expense&view_type=form`;
            }
            
            // Open expense form in new window/tab
            const newWindow = window.open(expenseUrl, '_blank');
            
            if (!newWindow) {
                // If popup blocked, show error
                this.notification.add(
                    _t("Please allow popups to open the expense form."),
                    { type: 'warning' }
                );
                return;
            }

            this.notification.add(
                _t("Expense form opened. Please complete and save the expense."),
                { type: 'success' }
            );
            
            // Close the popup
            this.props.close();
        } catch (error) {
            // Error is already shown by the RPC call with showErrorDialog=true
            console.error("Error opening expense form:", error);
        }
    },
});

