from odoo import models, fields, api

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('qris_manual', 'QRIS Manual')], ondelete={'qris_manual': 'set default'})
    qris_master_id = fields.Many2one('qris.payload.master', string='QRIS Master Source', 
                                     help="The specific QRIS data to use for generation")
    
    # Payment Logo Configuration
    payment_logo_type = fields.Selection([
        ('bank', 'Bank'),
        ('ewallet', 'E-Wallet')
    ], string='Payment Logo Type', help="Select whether this is a Bank or E-Wallet payment method")
    
    bank_name = fields.Selection([
        ('Aladin', 'Aladin'),
        ('Allo', 'Allo'),
        ('ANZ', 'ANZ'),
        ('Bangkok Bank', 'Bangkok Bank'),
        ('Bank BJB', 'Bank BJB'),
        ('Bank BPD Jateng', 'Bank BPD Jateng'),
        ('Bank of America', 'Bank of America'),
        ('Bank of China', 'Bank of China'),
        ('Bank of India', 'Bank of India'),
        ('Bank of India Indonesia', 'Bank of India Indonesia'),
        ('Bank Sahabat Sampoerna', 'Bank Sahabat Sampoerna'),
        ('BCA', 'BCA'),
        ('Blu BCA', 'Blu BCA'),
        ('BNC', 'BNC'),
        ('BNI', 'BNI'),
        ('BRI', 'BRI'),
        ('BSI', 'BSI'),
        ('BTN', 'BTN'),
        ('BTN (Alt)', 'BTN (Alt)'),
        ('BTN (New)', 'BTN (New)'),
        ('BTN Syariah', 'BTN Syariah'),
        ('BTN Syariah (New)', 'BTN Syariah (New)'),
        ('BTPN', 'BTPN'),
        ('CIMB Niaga', 'CIMB Niaga'),
        ('Citibank', 'Citibank'),
        ('Citibank (Alt)', 'Citibank (Alt)'),
        ('Commonwealth', 'Commonwealth'),
        ('Credit Suisse', 'Credit Suisse'),
        ('Danamon', 'Danamon'),
        ('DBS', 'DBS'),
        ('Deutsche Bank', 'Deutsche Bank'),
        ('HSBC', 'HSBC'),
        ('ICBC', 'ICBC'),
        ('Jago', 'Jago'),
        ('Jenius', 'Jenius'),
        ('JP Morgan Chase', 'JP Morgan Chase'),
        ('KB Bukopin', 'KB Bukopin'),
        ('Krom', 'Krom'),
        ('LINE Bank', 'LINE Bank'),
        ('Mandiri', 'Mandiri'),
        ('Maybank', 'Maybank'),
        ('Mega', 'Mega'),
        ('MNC', 'MNC'),
        ('Mualamat', 'Mualamat'),
        ('MUFG', 'MUFG'),
        ('MUFG (Alt)', 'MUFG (Alt)'),
        ('NOBU', 'NOBU'),
        ('OCBC NISP', 'OCBC NISP'),
        ('PaninBank', 'PaninBank'),
        ('Permata', 'Permata'),
        ('SeaBank', 'SeaBank'),
        ('Shinhan Bank', 'Shinhan Bank'),
        ('Sinarmas', 'Sinarmas'),
        ('Standard Chartered', 'Standard Chartered'),
        ('Superbank', 'Superbank'),
        ('UOB', 'UOB'),
    ], string='Bank Name')
    
    ewallet_name = fields.Selection([
        ('Astra Pay', 'Astra Pay'),
        ('Bluepay', 'Bluepay'),
        ('DANA', 'DANA'),
        ('Dipay', 'Dipay'),
        ('DOKU', 'DOKU'),
        ('Dutamoney', 'Dutamoney'),
        ('Gopay', 'Gopay'),
        ('I.Saku', 'I.Saku'),
        ('JakOne Pay', 'JakOne Pay'),
        ('Kaspro', 'Kaspro'),
        ('LinkAja', 'LinkAja'),
        ('Motion Pay', 'Motion Pay'),
        ('Netzme', 'Netzme'),
        ('OTTO Pay', 'OTTO Pay'),
        ('OVO (New Alt)', 'OVO (New Alt)'),
        ('Paydia', 'Paydia'),
        ('Paytren', 'Paytren'),
        ('Pospay', 'Pospay'),
        ('Shopee Pay', 'Shopee Pay'),
        ('SpeedCash', 'SpeedCash'),
        ('TrueMoney', 'TrueMoney'),
        ('Uangku', 'Uangku'),
        ('Yukk', 'Yukk'),
    ], string='E-Wallet Name')

    @api.model
    def _get_compatible_providers(self, *args, is_validation=False, **kwargs):
        """ Override to ensure QRIS Manual is available """
        providers = super()._get_compatible_providers(*args, is_validation=is_validation, **kwargs)
        
        if is_validation:
            return providers.filtered(lambda p: p.code != 'qris_manual')

        # Force Include QRIS Manual if not present (Debug/Fix)
        if 'qris_manual' not in providers.mapped('code'):
            qris = self.search([('code', '=', 'qris_manual'), ('state', '!=', 'disabled')], limit=1)
            if qris:
                providers |= qris
        
        return providers

    @api.model
    def action_fix_qris_manual_setup(self):
        """ Ensure QRIS Manual is fully configured and linked. Called via XML. """
        # 1. Ensure Payment Method
        method_code = 'qris_manual'
        method = self.env['payment.method'].search([('code', '=', method_code)], limit=1)
        if not method:
            method = self.env['payment.method'].create({
                'name': 'QRIS Manual',
                'code': method_code,
                'supported_country_ids': [(5, 0, 0)],
                'supported_currency_ids': [(5, 0, 0)],
            })
        
        # 2. Ensure Provider
        provider = self.search([('code', '=', 'qris_manual')], limit=1)
        if provider:
            # 3. Force Link
            if method.id not in provider.payment_method_ids.ids:
                provider.write({'payment_method_ids': [(4, method.id)]})
            
            # 4. Force Publish & Configuration
            provider.write({
                'state': 'test' if provider.state == 'disabled' else provider.state,
                'is_published': True,
                # 'company_id': False, # Must not be False if required
                'website_id': False,
                'available_country_ids': [(5, 0, 0)],
                'maximum_amount': 0.0,
            })
        return True

    def _get_supported_currencies(self):
        """ Allow all currencies? QRIS usually IDR. """
        self.ensure_one()
        if self.code == 'qris_manual':
             # Return IDR only if strict, but let's allow all for now or filter by master
             return super()._get_supported_currencies()
        return super()._get_supported_currencies()
