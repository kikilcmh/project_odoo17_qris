from odoo import models, fields, api

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    qris_log_id = fields.Many2one('qris.payload.log', string="QRIS Log", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        payments = super().create(vals_list)
        for payment in payments:
            if payment.qris_log_id:
                payment.qris_log_id.mark_as_paid_pos(payment.pos_order_id.id)
        return payments
