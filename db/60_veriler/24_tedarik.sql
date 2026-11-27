-- ============================================================================
-- Dosya   : db/60_veriler/24_tedarik.sql
-- Modul   : M4 Ilac & Tedarik
-- Sahibi  : Altyn Baktybekova (032390093)
-- Aciklama: Tedarik ornek verileri (tedarikci, eczane, ilac numaralari
--           13_eczane, 14_ilac ve 15_tedarikci dosyalarindaki sirayla eslesir).
-- Notlar  : - Tarihler 01.08.2026 - 20.11.2026 arasindadir; satislardan
--             (23_satis) once stok olussun diye cogu Eylul oncesidir.
--           - 14 ve 15 numarali ilaclar ile 12 numarali tedarikci bilerek
--             hic tedarik edilmedi (LEFT JOIN / NOT EXISTS sorgulari icin).
--           - trg_tedarik_denetim veriden once kuruldugu icin bu satirlarin
--             her biri tedarik_denetim tablosuna 'INSERT' olarak loglanir.
-- ============================================================================

INSERT INTO tedarik (tedarikci_no, eczane_no, ilac_no, miktar, tedarik_tarihi) VALUES
    (1,  1,  1,  200, '2026-08-03'),
    (1,  1,  2,  120, '2026-08-03'),
    (1,  2,  1,  150, '2026-08-10'),
    (1,  3,  3,   60, '2026-08-17'),
    (2,  2,  4,   80, '2026-08-05'),
    (2,  4,  5,   90, '2026-08-12'),
    (2,  5,  1,  180, '2026-08-19'),
    (2,  6,  6,  100, '2026-09-02'),
    (3,  3,  7,   70, '2026-08-07'),
    (3,  7,  8,   50, '2026-08-21'),
    (3,  8,  2,  110, '2026-09-04'),
    (4,  4,  9,   40, '2026-08-14'),
    (4,  9,  10,  65, '2026-08-28'),
    (4,  10, 1,  220, '2026-09-11'),
    (5,  5,  11,  45, '2026-08-09'),
    (5,  11, 3,   55, '2026-08-30'),
    (6,  6,  12,  30, '2026-08-16'),
    (6,  11, 6,   75, '2026-09-06'),
    (7,  12, 13,  85, '2026-08-23'),
    (7,  12, 1,  160, '2026-09-13'),
    (8,  13, 4,   95, '2026-08-25'),
    (8,  14, 5,   60, '2026-09-15'),
    (9,  15, 7,   50, '2026-09-01'),
    (9,  1,  9,   35, '2026-10-06'),
    (10, 6,  2,  140, '2026-10-13'),
    (10, 7,  1,  190, '2026-10-20'),
    (11, 8,  11,  40, '2026-11-03'),
    (11, 2,  12,  25, '2026-11-17');
