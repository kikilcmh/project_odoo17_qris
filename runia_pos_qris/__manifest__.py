{
    'name': 'POS QRIS Integration',
    'version': '1.1',
    'category': 'Point of Sale',
    'summary': 'Integrate Dynamic QRIS with Odoo POS',
    'description': """
        This module integrates functionality from runia_qris_generator into Point of Sale.
        - Adds QRIS Payment Method
        - Generates Dynamic QRIS on POS Payment Screen
        - Logs transactions to qris.payload.log
    """,
    'author': 'Runia',
    'depends': ['point_of_sale', 'runia_qris_generator'],
    'data': [
        'views/pos_payment_method_views.xml',
    ],
    'assets': {
        'point_of_sale.assets_prod': [
            'runia_pos_qris/static/lib/qrcode.min.js',
            'runia_pos_qris/static/src/app/debug_force.js',
            'runia_pos_qris/static/src/app/runia_pos_qris_models.js',
            'runia_pos_qris/static/src/app/runia_pos_qris_popup.js',
            'runia_pos_qris/static/src/app/runia_pos_qris_screen.js',
            'runia_pos_qris/static/src/xml/runia_qris_popup.xml',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}
