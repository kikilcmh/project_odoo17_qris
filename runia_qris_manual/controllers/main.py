import base64
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError

class QrisManualController(http.Controller):
    _redirect_url = '/payment/qris_manual/pay'
    _upload_url = '/payment/qris_manual/upload'

    @http.route(_redirect_url, type='http', auth='public', website=True, sitemap=False)
    def qris_manual_pay(self, reference, **kwargs):
        """ Render the QR Code page """
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
        if not tx:
            return request.redirect('/shop/payment')

        # Ensure QR Log exists
        if not tx.qris_log_id:
            master = tx.provider_id.qris_master_id
            if not master:
                 # Fallback or Error
                 return request.render('runia_qris_manual.error_page', {'error': 'QRIS Master not configured'})
            
            # Generate Dynamic Payload using Helper
            # The generate_dynamic method in master returns dict with payload and log_id
            # Log automatically handles unique code if logic is in create()
            
            # NOTE: Transaction Amount might not include the unique code yet. 
            # If we add unique code in Create(), the Amount in Log will be different from TX Amount.
            # This is fine. The user pays Log Amount.
            
            # Pass amount from TX.
            res = master.generate_dynamic(tx.amount, tx.reference, source='payment')
            log_id = res['log_id']
            tx.sudo().write({'qris_log_id': log_id})
        
        qris_log = tx.qris_log_id
        provider = tx.provider_id
        
        # Determine logo path based on provider configuration
        logo_path = None
        if provider.payment_logo_type == 'bank' and provider.bank_name:
            logo_path = f'/runia_qris_manual/static/src/img/banks/{provider.bank_name}.png'
        elif provider.payment_logo_type == 'ewallet' and provider.ewallet_name:
            logo_path = f'/runia_qris_manual/static/src/img/ewallet/{provider.ewallet_name}.png'
        
        # Render Template
        return request.render('runia_qris_manual.qris_payment_page', {
            'tx': tx,
            'qris_log': qris_log,
            'qris_payload': qris_log.dynamic_payload,
            'amount_display': qris_log.amount_total, # Display unique amount
            'upload_url': self._upload_url,
            'payment_logo_type': provider.payment_logo_type,
            'payment_logo_path': logo_path,
            'payment_logo_name': provider.bank_name or provider.ewallet_name,
        })

    @http.route(_upload_url, type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def qris_manual_upload(self, **post):
        """ Handle proof upload """
        reference = post.get('reference')
        proof_file = post.get('proof_file') # FileStorage
        
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
        if not tx or not tx.qris_log_id:
            return request.redirect('/shop/payment')

        if proof_file:
            file_content = proof_file.read()
            tx.qris_log_id.sudo().write({
                'proof_image': base64.b64encode(file_content),
                'proof_filename': proof_file.filename,
                'state': 'waiting_verification'
            })
            
            # Update Transaction State to Pending
            tx._process_notification_data({'status': 'waiting_verification', 'reference': reference})
            
            # Post to Invoice Chatter if invoice exists
            if tx.invoice_ids:
                invoice = tx.invoice_ids[0]
                
                # Create attachment for invoice
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': proof_file.filename,
                    'datas': base64.b64encode(file_content),
                    'res_model': 'account.move',
                    'res_id': invoice.id,
                    'type': 'binary',
                })
                
                # Format amount for display
                amount_str = "{:,.0f}".format(tx.qris_log_id.amount_total)
                
                # Post message to invoice chatter
                invoice.sudo().message_post(
                    body=f"""
                        <p><strong>Bukti Pembayaran QRIS Diterima</strong></p>
                        <ul>
                            <li>Referensi Transaksi: <strong>{reference}</strong></li>
                            <li>Jumlah: <strong>Rp {amount_str}</strong></li>
                            <li>Status: Menunggu Verifikasi</li>
                        </ul>
                    """,
                    subject="QRIS Payment Proof",
                    attachment_ids=[attachment.id],
                    message_type='comment',
                )

            # Redirect to generic confirmation or stay to show status
            return request.render('runia_qris_manual.qris_success_page', {'tx': tx})

        return request.redirect('/payment/qris_manual/pay?reference=%s' % reference)
