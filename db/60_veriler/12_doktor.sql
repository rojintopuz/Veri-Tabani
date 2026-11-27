-- ============================================================
-- Dosya   : db/60_veriler/12_doktor.sql
-- Modul   : M2 Doktor & Recete
-- Sahibi  : Meltem Can (032490033)
-- Aciklama: Doktor tablosu icin ornek veriler
-- Notlar  : - doktor_no otomatik 1-12 verilir; 21_muayene.sql 1-10'u kullanir.
--           - 11 ve 12 numarali doktorlar bilerek hic muayene/recete
--             yazmadi (NOT EXISTS / LEFT JOIN sorgulari icin).
-- ============================================================

INSERT INTO doktor (ad, uzmanlik_alani, deneyim_yili) VALUES
    ('Dr. Ali Yılmaz',       'İç Hastalıkları',         18),
    ('Dr. Ayşe Kara',        'Kardiyoloji',             22),
    ('Dr. Mehmet Öztürk',    'Ortopedi',                12),
    ('Dr. Zehra Aksoy',      'Kulak Burun Boğaz',        9),
    ('Dr. Can Şimşek',       'Endokrinoloji',           15),
    ('Dr. Elif Güneş',       'Aile Hekimliği',           6),
    ('Dr. Hasan Çetin',      'Göğüs Hastalıkları',      27),
    ('Dr. Gül Erdoğan',      'Psikiyatri',              11),
    ('Dr. Murat Koç',        'Enfeksiyon Hastalıkları',  8),
    ('Dr. Seda Yavuz',       'Gastroenteroloji',        14),
    ('Dr. Oğuz Tekin',       'Nöroloji',                 3),
    ('Dr. Deniz Uçar',       'Dermatoloji',              0);
