# Runia QRIS Manual Payment

Provides a QRIS payment method with manual verification.

## Features
1.  **Dynamic QRIS Generation**: Uses `runia_qris_generator` to create valid QRIS strings.
2.  **Manual Verification Flow**:
    - User selects "QRIS Manual" at checkout / portal.
    - Redirected to a page showing the QR Code and the **Unique Amount**.
    - User scans and pays the exact amount.
    - User uploads proof of payment on the same page.
    - Status changes to `Waiting Verification`.
    - Admin reviews in "Verification Queue" and verifies.
    - Sales Order / Invoice marks as Paid.
3.  **Unique Code Logic**: Automatically adds a unique code (1-300) to the transaction amount to differentiate identical amounts from different customers.
4.  **Proof of Payment**: Mandatory image upload. Without upload, state remains "Pending".

## Configuration
1.  Go to **Accounting / Payment Providers**.
2.  Select **QRIS Manual**.
3.  Set State to **Test** or **Enabled**.
4.  Set **QRIS Master Source** (the `qris.payload.master` record to use).
5.  Publish the provider.

## Usage
### User Side
1.  Checkout -> Select "QRIS Manual" -> Pay.
2.  Page redirects to `/payment/qris_manual/pay`.
3.  QR Code is displayed.
4.  Upload Proof -> Submit.

### Admin Side
1.  Go to **Apps -> QRIS Generator -> Verification Queue** (or Search Transaction Log).
2.  Open record with status `Waiting Verification`.
3.  Check `Proof Image` against `Total Amount`.
4.  Click **Verify & Mark Paid**.
5.  Linked Payment Transaction updates to `Confirmed`.
