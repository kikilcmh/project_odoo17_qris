# Runia QRIS Odoo 17 Modules

This repository contains a suite of Odoo 17 modules for integrating QRIS (Quick Response Code Indonesian Standard) payments into the Odoo ecosystem. It supports both Point of Sale (POS) and manual payment workflows with dynamic QR code generation.

## Modules Overview

### 1. Runia QRIS Generator (`runia_qris_generator`)
**Core Utility Module**

This is the foundational module that handles the backend logic for QRIS payload management.
- **Features:**
    - Stores Static QRIS Payload Master data.
    - Generates Dynamic QRIS Payloads by injecting transaction amounts.
    - Computes CRC16 CCITT for payload validation.
    - Logs all generated QRIS payloads for audit trails.
    - Includes a convenient "Tester Wizard" to verify QR code generation.

### 2. POS QRIS Integration (`runia_pos_qris`)
**Point of Sale Extension**

This module extends the Odoo Point of Sale to support QRIS payments directly at the cashier.
- **Features:**
    - Adds a dedicated "QRIS" payment method in POS.
    - Generates a dynamic QR code on the POS display for customers to scan.
    - Integrates with `runia_qris_generator` for accurate payload creation.
    - Logs transactions automatically.

### 3. Runia QRIS Manual Payment (`runia_qris_manual`)
**eCommerce & Invoice Payment Provider**

This module allows customers to pay via QRIS for online orders or invoices with a manual verification step.
- **Features:**
    - Generates dynamic QRIS codes for web checkout and invoices.
    - **Unique Code System:** Adds a unique random code (1-300) to the transaction amount to facilitate easier manual reconciliation.
    - **Proof of Payment:** Requires customers to upload a transfer proof (image) after scanning.
    - Admin dashboard for manual verification and confirmation of payments.

## Installation

1. Clone this repository to your Odoo addons path:
   ```bash
   git clone https://github.com/kikilcmh/project_odoo17_qris.git
   ```
2. Update your Odoo configuration file (`odoo.conf`) to include the new addons path.
3. Restart the Odoo service.
4. Go to **Apps**, click **Update Apps List**, and install the modules in the following order:
   - `runia_qris_generator` (Required Core)
   - `runia_qris_manual` (Optional)
   - `runia_pos_qris` (Optional)

## Requirements
- Odoo 17.0
- Python libraries: `qrcode` (for QR generation if not already included in your Odoo env)

## License
LGPL-3
