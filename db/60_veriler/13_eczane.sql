-- ============================================================================
-- Dosya   : db/60_veriler/13_eczane.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Eczane ve eczane_telefon tablolari icin ornek veriler
-- ============================================================================

INSERT INTO eczane (ad, adres) VALUES
    ('Merkez Şifa Eczanesi', 'Atatürk Cad. No: 14, Osmangazi / Bursa'),
    ('Görükle Kampüs Eczanesi', 'Sakarya Mah. Üniversite Bulv. No: 42, Nilüfer / Bursa'),
    ('Nilüfer Park Eczanesi', 'Fethiye Mah. Fatih Sultan Mehmet Bulv. No: 88, Nilüfer / Bursa'),
    ('Uludağ Hayat Eczanesi', 'İhsaniye Mah. Tuna Cad. No: 19, Nilüfer / Bursa'),
    ('Yıldırım Sağlık Eczanesi', 'Ankara Yolu Cad. No: 112, Yıldırım / Bursa'),
    ('Mudanya Sahil Eczanesi', 'Halitpaşa Mah. İskele Meydanı No: 7, Mudanya / Bursa'),
    ('Çekirge Termal Eczanesi', 'Çekirge Cad. No: 63, Osmangazi / Bursa'),
    ('Beşevler Derman Eczanesi', 'Beşevler Mah. Bilginler Cad. No: 25, Nilüfer / Bursa'),
    ('Özlüce Modern Eczanesi', 'Özlüce Mah. Ahmet Taner Kışlalı Bulv. No: 51, Nilüfer / Bursa'),
    ('Emek Güney Eczanesi', 'Emek Adnan Menderes Mah. Turgut Özal Cad. No: 33, Osmangazi / Bursa'),
    ('Gemlik Körfez Eczanesi', 'Dr. Ziya Kaya Mah. Orhangazi Cad. No: 18, Gemlik / Bursa'),
    ('İnegöl Merkez Eczanesi', 'Cuma Mah. Atatürk Bulv. No: 74, İnegöl / Bursa'),
    ('Kükürtlü Lokman Eczanesi', 'Kükürtlü Cad. No: 29, Osmangazi / Bursa'),
    ('Ertuğrul Kent Eczanesi', 'Ertuğrul Mah. Uğur Mumcu Bulv. No: 60, Nilüfer / Bursa'),
    ('Altınşehir Eczanesi', 'Altınşehir Mah. Muammer Aksoy Cad. No: 11, Nilüfer / Bursa');

INSERT INTO eczane_telefon (eczane_no, telefon_no) VALUES
    (1, '02242211001'),
    (1, '02242211002'),
    (2, '02244832001'),
    (2, '05324832002'),
    (3, '02242453001'),
    (3, '02242453002'),
    (4, '02242494001'),
    (4, '05332494002'),
    (5, '02243615001'),
    (5, '02243615002'),
    (6, '02245446001'),
    (6, '05355446002'),
    (7, '02242337001'),
    (7, '02242337002'),
    (8, '02244518001'),
    (8, '05364518002'),
    (9, '02244139001'),
    (9, '02244139002'),
    (10, '02242421010'),
    (10, '05372421011'),
    (11, '02245131101'),
    (11, '02245131102'),
    (12, '02247151201'),
    (12, '05387151202'),
    (13, '02242351301'),
    (13, '02242351302'),
    (14, '02244141401'),
    (14, '05394141402'),
    (15, '02244121501'),
    (15, '02244121502');