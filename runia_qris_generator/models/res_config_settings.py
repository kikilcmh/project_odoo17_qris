from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Add settings fields here if needed in the future
    qris_tester_placeholder = fields.Boolean(string="Enable QRIS Tester", default=True)
