from odoo import fields, models

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    use_qris_generator = fields.Boolean(string="Use QRIS Generator")
    qris_master_id = fields.Many2one('qris.payload.master', string="QRIS Master Data")
