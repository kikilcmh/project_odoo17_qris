/** @odoo-module */
import { Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

console.log("Runia QRIS 🚀: runia_pos_qris_models.js LOADED (Renamed)");

patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.qris_log_id = this.qris_log_id || null;
        this.qris_payload = this.qris_payload || null;
        console.log("Runia QRIS 🚀: Payment Model Initialized", {
            method: this.payment_method?.name,
            use_qris: this.payment_method?.use_qris_generator,
            master_id: this.payment_method?.qris_master_id
        });
    },
    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.qris_log_id = this.qris_log_id;
        return json;
    },
    set_qris_log_id(id) {
        this.qris_log_id = id;
    },
    set_qris_payload(payload) {
        this.qris_payload = payload;
    }
});
