from odoo import fields, models, api

class QrisPayloadLog(models.Model):
    _inherit = 'qris.payload.log'

    pos_order_id = fields.Many2one('pos.order', string="POS Order")

    def mark_as_paid_pos(self, pos_order_id):
        """
        API for POS to mark logic as paid and link to order
        """
        self.ensure_one()
        self.write({
            'state': 'paid',
            'pos_order_id': pos_order_id
        })
        return True
