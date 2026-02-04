from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class QrisPayloadMaster(models.Model):
    _name = 'qris.payload.master'
    _description = 'QRIS Payload Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    merchant_id = fields.Char(string='Merchant ID', help="Optional merchant identification")
    static_payload = fields.Text(string='Static Payload', required=True, tracking=True)
    active = fields.Boolean(default=True)

    @api.constrains('static_payload')
    def _check_payload_format(self):
        for record in self.filtered(lambda r: r.static_payload):
            if not record.static_payload.startswith('000201'):
                # Basic QRIS check
                pass

    def generate_dynamic(self, amount, reference, source='pos'):
        """
        Contract:
        - generate_dynamic(amount, reference) -> payload, log_id
        """
        _logger.info("Runia QRIS 🚀: generate_dynamic called for amount %s, reference %s", amount, reference)
        self.ensure_one()
        from .qris_tools import static_to_dynamic
        
        # 1. Generate Payload
        new_payload = static_to_dynamic(self.static_payload, str(amount))
        
        # 2. Create Log (Draft)
        log = self.env['qris.payload.log'].create({
            'master_id': self.id,
            'amount': amount,
            'dynamic_payload': new_payload,
            'source': source,
            'reference': reference,
            'state': 'draft',
        })
        
        _logger.info("Runia QRIS 🚀: Log created %s", log.id)
        
        return {
            'payload': new_payload,
            'log_id': log.id,
        }
