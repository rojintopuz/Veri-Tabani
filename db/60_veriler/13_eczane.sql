-- ============================================================================
-- Dosya   : db/60_veriler/13_eczane.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Eczane ve eczane_telefon tablolari icin ornek veriler
-- ============================================================================

INSERT INTO eczane (ad, adres) VALUES
    ('Merkez Sifa Eczanesi', 'Ataturk Cad. No: 14, Osmangazi / Bursa'),
    ('Gorukle Kampus Eczanesi', 'Sakarya Mah. Universite Bulv. No: 42, Nilufer / Bursa'),
    ('Nilufer Park Eczanesi', 'Fethiye Mah. Fatih Sultan Mehmet Bulv. No: 88, Nilufer / Bursa'),
    ('Uludag Hayat Eczanesi', 'Ihsaniye Mah. Tuna Cad. No: 19, Nilufer / Bursa'),
    ('Yildirim Saglik Eczanesi', 'Ankara Yolu Cad. No: 112, Yildirim / Bursa'),
    ('Mudanya Sahil Eczanesi', 'Halitpasa Mah. Iskele Meydani No: 7, Mudanya / Bursa'),
    ('Cekirge Termal Eczanesi', 'Cekirge Cad. No: 63, Osmangazi / Bursa'),
    ('Besevler Derman Eczanesi', 'Besevler Mah. Bilginler Cad. No: 25, Nilufer / Bursa'),
    ('Ozluce Modern Eczanesi', 'Ozluce Mah. Ahmet Taner Kislali Bulv. No: 51, Nilufer / Bursa'),
    ('Emek Guney Eczanesi', 'Emek Adnan Menderes Mah. Turgut Ozal Cad. No: 33, Osmangazi / Bursa'),
    ('Gemlik Korfez Eczanesi', 'Dr. Ziya Kaya Mah. Orhangazi Cad. No: 18, Gemlik / Bursa'),
    ('Inegol Merkez Eczanesi', 'Cuma Mah. Ataturk Bulv. No: 74, Inegol / Bursa'),
    ('Kukurtlu Lokman Eczanesi', 'Kukurtlu Cad. No: 29, Osmangazi / Bursa'),
    ('Ertugrul Kent Eczanesi', 'Ertugrul Mah. Ugur Mumcu Bulv. No: 60, Nilufer / Bursa'),
    ('Altinsehir Eczanesi', 'Altinsehir Mah. Muammer Aksoy Cad. No: 11, Nilufer / Bursa');

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