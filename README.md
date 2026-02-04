# Runia QRIS Odoo 17 Modules

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

---

<a name="english"></a>
## 🇬🇧 English

This repository contains a suite of Odoo 17 modules for integrating QRIS (Quick Response Code Indonesian Standard) payments into the Odoo ecosystem. It supports both Point of Sale (POS) and manual payment workflows with dynamic QR code generation.

### Key Functions
- **Unified QRIS Payments:** Accept QRIS payments across Odoo Point of Sale (POS), Invoices, and eCommerce.
- **Static to Dynamic Conversion:** Converts your master Static QRIS code into unique Dynamic QRIS codes for every transaction.
- **Manual Verification Helper:** Uses a unique code system (random last digits) to facilitate easy manual reconciliation for bank transfers.
- **Proof of Payment:** Integrated workflow for verifying customer payment execution.

### Modules Overview

#### 1. Runia QRIS Generator (`runia_qris_generator`)
**Core Utility Module**

This is the foundational module that handles the backend logic for QRIS payload management.
- **Features:**
    - Stores Static QRIS Payload Master data.
    - Generates Dynamic QRIS Payloads by injecting transaction amounts.
    - Computes CRC16 CCITT for payload validation.
    - Logs all generated QRIS payloads for audit trails.
    - Includes a convenient "Tester Wizard" to verify QR code generation.

#### 2. POS QRIS Integration (`runia_pos_qris`)
**Point of Sale Extension**

This module extends the Odoo Point of Sale to support QRIS payments directly at the cashier.
- **Features:**
    - Adds a dedicated "QRIS" payment method in POS.
    - Generates a dynamic QR code on the POS display for customers to scan.
    - Integrates with `runia_qris_generator` for accurate payload creation.
    - Logs transactions automatically.

#### 3. Runia QRIS Manual Payment (`runia_qris_manual`)
**eCommerce & Invoice Payment Provider**

This module allows customers to pay via QRIS for online orders or invoices with a manual verification step.
- **Features:**
    - Generates dynamic QRIS codes for web checkout and invoices.
    - **Unique Code System:** Adds a unique random code (1-300) to the transaction amount to facilitate easier manual reconciliation.
    - **Proof of Payment:** Requires customers to upload a transfer proof (image) after scanning.
    - Admin dashboard for manual verification and confirmation of payments.

### Installation

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

### Requirements
- Odoo 17.0
- Python libraries: `qrcode` (for QR generation if not already included in your Odoo env)

### License
LGPL-3

---

<a name="bahasa-indonesia"></a>
## 🇮🇩 Bahasa Indonesia

Repositori ini berisi kumpulan modul Odoo 17 untuk mengintegrasikan pembayaran QRIS (Quick Response Code Indonesian Standard) ke dalam ekosistem Odoo. Mendukung alur kerja kasir (POS) maupun pembayaran manual dengan pembuatan kode QR dinamis.

### Fungsi Utama
- **Pembayaran QRIS Terpadu:** Menerima pembayaran QRIS di Odoo Point of Sale (POS), Invoice, dan eCommerce.
- **Konversi Statis ke Dinamis:** Mengubah master QRIS Statis Anda menjadi QRIS Dinamis unik untuk setiap transaksi.
- **Bantuan Verifikasi Manual:** Menggunakan sistem kode unik (digit terakhir acak) untuk memudahkan rekonsiliasi manual transfer bank.
- **Bukti Pembayaran:** Alur kerja terintegrasi untuk memverifikasi eksekusi pembayaran pelanggan.

### Ringkasan Modul

#### 1. Runia QRIS Generator (`runia_qris_generator`)
**Modul Utilitas Inti**

Ini adalah modul dasar yang menangani logika backend untuk pengelolaan payload QRIS.
- **Fitur:**
    - Menyimpan data Master Payload QRIS Statis.
    - Menghasilkan Payload QRIS Dinamis dengan menyuntikkan nominal transaksi.
    - Menghitung CRC16 CCITT untuk validasi payload.
    - Mencatat log semua payload QRIS yang dibuat untuk audit.
    - Dilengkapi fitur "Tester Wizard" untuk menguji pembuatan kode QR.

#### 2. POS QRIS Integration (`runia_pos_qris`)
**Ekstensi Point of Sale**

Modul ini memperluas fungsi Odoo Point of Sale untuk mendukung pembayaran QRIS langsung di kasir.
- **Fitur:**
    - Menambahkan metode pembayaran khusus "QRIS" di POS.
    - Menampilkan kode QR dinamis di layar POS agar dapat dipindai oleh pelanggan.
    - Terintegrasi dengan `runia_qris_generator` untuk pembuatan payload yang akurat.
    - Mencatat transaksi secara otomatis.

#### 3. Runia QRIS Manual Payment (`runia_qris_manual`)
**Penyedia Pembayaran eCommerce & Invoice**

Modul ini memungkinkan pelanggan membayar melalui QRIS untuk pesanan online atau tagihan dengan langkah verifikasi manual.
- **Fitur:**
    - Membuat kode QRIS dinamis untuk checkout web dan invoice.
    - **Sistem Kode Unik:** Menambahkan kode acak unik (1-300) pada nominal transaksi untuk memudahkan rekonsiliasi manual.
    - **Bukti Pembayaran:** Mewajibkan pelanggan mengunggah bukti transfer (gambar) setelah memindai.
    - Dasbor admin untuk verifikasi dan konfirmasi pembayaran manual.

### Instalasi

1. Clone repositori ini ke path addons Odoo Anda:
   ```bash
   git clone https://github.com/kikilcmh/project_odoo17_qris.git
   ```
2. Update file konfigurasi Odoo Anda (`odoo.conf`) untuk memasukkan path addons baru.
3. Restart service Odoo.
4. Buka **Apps**, klik **Update Apps List**, dan instal modul dengan urutan berikut:
   - `runia_qris_generator` (Inti - Wajib)
   - `runia_qris_manual` (Opsional)
   - `runia_pos_qris` (Opsional)

### Persyaratan
- Odoo 17.0
- Library Python: `qrcode` (untuk pembuatan QR jika belum ada di env Odoo Anda)

### Lisensi
LGPL-3
