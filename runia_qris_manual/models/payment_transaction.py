from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    qris_log_id = fields.Many2one('qris.payload.log', string='QRIS Transaction Log')

    def _get_specific_processing_values(self, processing_values):
        """ Return params for the payment form (redirect or custom) """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'qris_manual':
            return res

        # We can prepare the QR log here or in the controller.
        # If we do it here, we ensure 1 transaction = 1 QR immediately.
        # But `_get_specific_processing_values` is called when rendering the button "Pay".
        # Creating a log every time the button is rendered (e.g. if user refreshes) is bad?
        # Typically this is called when "Pay" is clicked if using "Redirect".
        # Let's rely on the Controller to generate/retrieve the log to avoid spamming logs.
        
        return res

    def _get_specific_rendering_values(self, processing_values):
        """ Return values for the redirect form """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'qris_manual':
            return res

        # URL to our controller that handles the actual QR display page
        base_url = self.provider_id.get_base_url()
        res['api_url'] = f'{base_url}/payment/qris_manual/pay'
        res['reference'] = self.reference
        return res

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Find transaction based on returned data """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'qris_manual' or len(tx) == 1:
            return tx
        
        reference = notification_data.get('reference')
        return self.search([('reference', '=', reference), ('provider_code', '=', 'qris_manual')])

    def _process_notification_data(self, notification_data):
        """ Handle state updates from controller """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'qris_manual':
            return

        status = notification_data.get('status')
        if status == 'waiting_verification':
            self._set_pending(state_message="Waiting for proof verification")
        elif status == 'paid':
            self._set_done()
        elif status == 'rejected':
             self._set_canceled(state_message="Proof rejected")
