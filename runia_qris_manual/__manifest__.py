{
    'name': 'Runia QRIS Manual Payment',
    'version': '1.0',
    'summary': 'Manual QRIS Payment Method with Proof Upload',
    'description': """
        Provides a dynamic QRIS payment method (Manual verification).
        - Generates Dynamic QRIS code using runia_qris_generator.
        - Adds Unique Code (1-300) to transaction amount.
        - Requires Proof of Payment upload (Image).
        - Admin manual verification flow.
    """,
    'category': 'Accounting/Payment Providers',
    'author': 'Runia',
    'depends': [
        'runia_qris_generator',
        'payment',
        'sale',
        'account',
        'website_sale', 
    ],
    'data': [
        'views/qris_log_views.xml',
        'views/payment_provider_views.xml',
        'views/payment_template.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'data/payment_provider_fix.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
