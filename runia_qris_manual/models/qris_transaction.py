from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class QrisPayloadLog(models.Model):
    _inherit = 'qris.payload.log'

    # Extend State
    state = fields.Selection(selection_add=[
        ('waiting_proof', 'Waiting Proof'),
        ('waiting_verification', 'Waiting Verification'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ], ondelete={'waiting_proof': 'set default', 'waiting_verification': 'set default', 'rejected': 'cascade', 'expired': 'cascade'})

    # Additional Fields
    unique_code = fields.Integer(string='Unique Code (1-300)', readonly=True)
    amount_total = fields.Monetary(string='Total Amount (Unique)', compute='_compute_amount_total', store=True, currency_field='currency_id')
    
    proof_image = fields.Binary(string='Payment Proof')
    proof_filename = fields.Char(string='Proof Filename')
    
    related_document = fields.Char(string='Related Document', help="Invoice or SO Number", index=True)

    @api.depends('amount', 'unique_code')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = record.amount + record.unique_code

    @api.model
    def create(self, vals):
        # [MODIFIED] Unique Code Disabled by User Request
        if 'unique_code' not in vals:
             vals['unique_code'] = 0 # self._get_next_unique_code()
        return super(QrisPayloadLog, self).create(vals)

    @api.model
    def _get_next_unique_code(self):
        # Find the last created record's unique code
        last_log = self.search([('unique_code', '>', 0)], order='create_date desc, id desc', limit=1)
        if not last_log:
            return 1
        
        next_code = last_log.unique_code + 1
        if next_code > 300:
            return 1
        return next_code

    def action_upload_proof(self):
        """ Allow user to upload proof from portal/view """
        self.ensure_one()
        if not self.proof_image:
            raise ValidationError(_("Please upload an image as proof of payment."))
        self.write({'state': 'waiting_verification'})
        # Optional: Notify admin

    transaction_ids = fields.One2many('payment.transaction', 'qris_log_id', string='Payment Transactions')

    def action_verify_paid(self):
        """ Admin marks as paid """
        self.ensure_one()
        if not self.proof_image:
             if not self._context.get('force_pay'):
                 raise ValidationError(_("Cannot mark as paid without proof image."))
        
        self.write({'state': 'paid'})
        self._post_payment_processing()

    def action_reject_proof(self):
        """ Admin rejects the proof """
        self.ensure_one()
        self.write({'state': 'rejected'})
        for tx in self.transaction_ids:
            tx._process_notification_data({'status': 'rejected', 'reference': tx.reference})
    
    def _post_payment_processing(self):
        """ Hook to update SO/Invoice status """
        for tx in self.transaction_ids:
            # We simulate a notification from the provider
            tx._process_notification_data({'status': 'paid', 'reference': tx.reference})
