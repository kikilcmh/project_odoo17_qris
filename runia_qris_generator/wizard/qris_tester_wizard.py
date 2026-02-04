from odoo import models, fields, api, _

class QrisTesterWizard(models.TransientModel):
    _name = 'qris.payload.tester.wizard'
    _description = 'QRIS Tester Wizard'

    # Move this to the top
    
    master_id = fields.Many2one('qris.payload.master', string='Select Master QRIS', required=True)
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    dynamic_payload = fields.Text(string='Dynamic Payload', readonly=True)
    qr_image = fields.Binary(string='QR Code Preview', readonly=True)

    def action_generate(self):
        self.ensure_one()
        import base64
        from ..models.qris_tools import static_to_dynamic
        
        new_payload = static_to_dynamic(self.master_id.static_payload, str(self.amount))
        
        # Generate QR Image using Odoo's native barcode generator (on the server side)
        # This is the most robust way to handle long payloads
        qr_data = self.env['ir.actions.report'].barcode('QR', new_payload, width=512, height=512)
        qr_base64 = base64.b64encode(qr_data)
        
        self.write({
            'dynamic_payload': new_payload,
            'qr_image': qr_base64
        })
        
        # Log the generation
        self.env['qris.payload.log'].create({
            'master_id': self.master_id.id,
            'amount': self.amount,
            'dynamic_payload': new_payload,
            'source': 'wizard',
            'reference': 'TEST/WIZARD/%s' % fields.Datetime.now(),
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
