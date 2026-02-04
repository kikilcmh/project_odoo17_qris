from odoo import models, fields, api

class QrisPayloadLog(models.Model):
    _name = 'qris.payload.log'
    _description = 'QRIS Payload Logo'
    _order = 'create_date desc'

    master_id = fields.Many2one('qris.payload.master', string='Master QRIS', ondelete='cascade')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    dynamic_payload = fields.Text(string='Generated Payload')
    source = fields.Selection([
        ('wizard', 'Tester Wizard'),
        ('pos', 'Point of Sale'),
        ('payment', 'Online Payment'),
    ], string='Source', default='wizard')
    reference = fields.Char(string='Reference', help="Order/Invoice/Transaction Reference")
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    created_on = fields.Datetime(string='Created On', default=fields.Datetime.now, readonly=True)
    state = fields.Selection([
        ('draft', 'Pending'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', required=True)

    def action_mark_paid(self):
        self.ensure_one()
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
