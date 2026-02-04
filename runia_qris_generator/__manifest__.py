{
    'name': 'Runia QRIS Generator',
    'version': '1.0',
    'summary': 'Core Utility for QRIS Static to Dynamic Payload Generation',
    'description': """
        This module provides core utilities to:
        - Store Static QRIS Payload Master
        - Generate Dynamic QRIS Payload (with amount injection)
        - Compute CRC16 CCITT
        - Log generated QRIS payloads
        - Tester Wizard for QRIS generation
    """,
    'author': 'Runia',
    'category': 'Hidden',
    'website': 'https://www.runia.id',
    'depends': ['base', 'mail', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/qris_payload_master_views.xml',
        'views/qris_payload_log_views.xml',
        'wizard/qris_tester_wizard_view.xml',
        'views/menu_items.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}
