/** @odoo-module */
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { RuniaQrisPopup } from "./runia_pos_qris_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";

console.log("Runia QRIS 🚀: runia_pos_qris_screen.js LOADED (Renamed)");

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },

    async addNewPaymentLine(paymentMethod) {
        console.log("Runia QRIS 🚀: addNewPaymentLine HIT!", {
            name: paymentMethod.name,
            use_qris: paymentMethod.use_qris_generator,
            master: paymentMethod.qris_master_id
        });

        // 1. Call super (Returns Boolean in Odoo 17)
        const result = super.addNewPaymentLine(paymentMethod);

        if (!result) {
            console.log("Runia QRIS 🚀: Super returned false");
            return false;
        }

        // 2. Check configuration
        if (paymentMethod.use_qris_generator) {
            console.log("Runia QRIS 🚀: QRIS Generator Enabled. Searching for created line...");

            // 3. Find the line we just added
            // It should be the last one for this method without a log_id
            const paymentLines = this.currentOrder.paymentlines;
            let line = null;

            // Robust finding strategy
            if (Array.isArray(paymentLines)) {
                line = paymentLines.find(pl => pl.payment_method.id === paymentMethod.id && !pl.qris_log_id);
            } else if (paymentLines.models) {
                // Collection fallback
                line = paymentLines.models.find(pl => pl.payment_method.id === paymentMethod.id && !pl.qris_log_id);
            }

            if (line) {
                console.log("Runia QRIS 🚀: Line Found!", line.cid);
                await this.handleQrisGeneration(line, paymentMethod);
            } else {
                console.warn("Runia QRIS 🚀: Line NOT found after creation.");
            }
        }

        return result;
    },

    async handleQrisGeneration(line, paymentMethod) {
        if (!paymentMethod.qris_master_id) {
            this.popup.add(ErrorPopup, { title: 'Configuration Error', body: 'QRIS Master not configured on this Payment Method' });
            this.currentOrder.remove_paymentline(line);
            return;
        }

        const amount = line.get_amount();
        const reference = this.currentOrder.name;

        // Validation: Positive amount
        if (amount <= 0) {
            this.popup.add(ErrorPopup, { title: 'Invalid Amount', body: 'QRIS can only be generated for positive amounts.' });
            this.currentOrder.remove_paymentline(line);
            return;
        }

        try {
            // Show loading if needed, but RPC is fast.
            const result = await this.orm.call(
                'qris.payload.master',
                'generate_dynamic',
                [paymentMethod.qris_master_id[0], amount, reference, 'pos']
            );

            line.set_qris_log_id(result.log_id);
            line.set_qris_payload(result.payload);

            const { confirmed } = await this.popup.add(RuniaQrisPopup, {
                title: "Scan QRIS",
                amount_text: this.env.utils.formatCurrency(amount),
                payload: result.payload
            });

            if (confirmed) {
                // User clicked "Selesai" - Payment is confirmed
                console.log("Runia QRIS 🚀: Payment confirmed by user");

                // Mark payment line as done
                line.set_payment_status('done');

                // Update backend log to 'paid'
                try {
                    await this.orm.call(
                        'qris.payload.log',
                        'action_mark_paid',
                        [[result.log_id]]
                    );
                    console.log("Runia QRIS 🚀: Backend log marked as paid");
                } catch (logError) {
                    console.warn("Runia QRIS ⚠️: Failed to update log status", logError);
                    // Continue anyway - frontend payment is what matters
                }

                // Trigger order validation → "Pembayaran Berhasil" screen
                await this.validateOrder(false, false);

            } else {
                // User clicked "Batal" - Remove payment line
                console.log("Runia QRIS 🚀: Payment cancelled by user");
                this.currentOrder.remove_paymentline(line);
            }

        } catch (error) {
            console.error(error);
            this.popup.add(ErrorPopup, { title: 'Generation Failed', body: error.message || 'Unknown error' });
            this.currentOrder.remove_paymentline(line);
        }
    }
});
