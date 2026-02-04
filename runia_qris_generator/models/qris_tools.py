import re

def crc16_ccitt(payload_str):
    """
    Kalkulasi CRC16-CCITT (Poly: 0x1021, Init: 0xFFFF)
    Hasil identik dengan logic di coba2.html
    """
    crc = 0xFFFF
    for char in payload_str:
        crc ^= (ord(char) << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')

def static_to_dynamic(qris_payload, amount_str):
    """
    Konversi QRIS Static ke Dynamic dengan proteksi karakter sampah (Odoo/Windows).
    """
    # 1. CLEANING: Buang semua karakter non-printable/hidden yang mungkin terbawa saat paste
    # Hanya izinkan angka, huruf besar, titik, spasi, dan persen (standar QRIS)
    qris = re.sub(r'[^0-9A-Z.% -]', '', str(qris_payload).upper().strip())
    amount_clean = re.sub(r'[^0-9]', '', str(amount_str).split('.')[0].split(',')[0])

    if not qris or not amount_clean:
        return qris

    # 2. STRIP OLD CRC: Cari kemunculan terakhir Tag '6304'
    # Kita tidak pakai [:-4] karena berbahaya jika ada spasi tersembunyi
    idx = qris.rfind('6304')
    if idx != -1:
        qris = qris[:idx+4] # Ambil string sampa dengan angka '6304' saja
    else:
        # Jika master tidak punya 6304, kita tambahkan manual agar logic rebuild tetap jalan
        if not qris.endswith('6304'):
             qris += '6304'

    # 3. POINT OF INITIATION: Ubah Static (010211) -> Dynamic (010212)
    qris = qris.replace("010211", "010212", 1)

    # 4. SPLIT & INJECT: Masukkan nominal (Tag 54) sebelum Tag Country Code (5802ID)
    if "5802ID" not in qris:
        # Fallback jika master aneh
        return qris

    parts = qris.split("5802ID", 1)
    # parts[0] = prefix s/d sebelum 5802ID
    # parts[1] = suffix mulai dari setelah 5802ID (biasanya nama merchant s/d 6304)

    # Bentuk Tag 54
    tag54 = "54" + str(len(amount_clean)).zfill(2) + amount_clean

    # 5. REBUILD: Ikuti urutan coba2.html
    # [Awal] + [Tag 54] + ["5802ID"] + [Sisa s/d 6304]
    result = parts[0] + tag54 + "5802ID" + parts[1]

    # 6. CALCULATE FINAL CRC
    # Karena result berakhir di '6304' (dari langkah 2 & 4), 
    # kita tinggal hitung CRC dari seluruh string tersebut dan tempel.
    final_crc = crc16_ccitt(result)
    
    return result + final_crc
