/** @odoo-module */
console.log("Runia QRIS 🚀: runia_pos_qris_popup.js LOADED (Renamed)");
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { onMounted, useRef, Component } from "@odoo/owl";

// Ensure this component is registered if Odoo requires it, though usually AbstractAwaitablePopup handles it via the screen.

export class RuniaQrisPopup extends AbstractAwaitablePopup {
    static template = "runia_pos_qris.RuniaQrisPopup";
    static defaultProps = {
        confirmText: _t("Done"),
        cancelText: _t("Cancel"),
        title: _t("QRIS Payment"),
        payload: "",
        amount_text: ""
    };

    setup() {
        super.setup();
        this.qrCodeRef = useRef("qrcode");
        onMounted(() => {
            this.renderQrCode();
        });
    }

    renderQrCode() {
        if (this.props.payload && this.qrCodeRef.el) {
            // Clean previous
            this.qrCodeRef.el.innerHTML = '';

            // Setup QRCode
            // Note: QRCode is globally available thanks to point_of_sale assets
            try {
                new QRCode(this.qrCodeRef.el, {
                    text: this.props.payload,
                    width: 256,
                    height: 256,
                    colorDark: "#000000",
                    colorLight: "#ffffff",
                    correctLevel: QRCode.CorrectLevel.H
                });
            } catch (e) {
                console.error("QR Code Generation Error", e);
                this.qrCodeRef.el.innerText = "Error Generating QR";
            }
        }
    }
}
