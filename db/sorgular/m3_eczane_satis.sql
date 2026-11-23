-- ============================================================================
-- Dosya   : db/sorgular/m3_eczane_satis.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Eczane ve satis modulu icin 6 is sorgusu
-- ============================================================================

-- S1 (a - >=3 tablolu JOIN)
-- Soru: Her satista hangi eczane hangi hastaya hangi ilaci kac liraya ve ne zaman satmistir?
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    h.ad AS hasta_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN hasta AS h ON h.hasta_kimlik_no = s.hasta_kimlik_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
ORDER BY s.satis_tarihi DESC, s.satis_id DESC;

-- S2 (b - GROUP BY + HAVING)
-- Soru: En az 2 satis yapmis ve toplam cirosu 200 TL uzerinde olan eczanelerin satis sayisi ve toplam cirosu nedir?
SELECT
    e.eczane_no,
    e.ad AS eczane_ad,
    COUNT(s.satis_id) AS satis_sayisi,
    SUM(s.fiyat) AS toplam_ciro
FROM eczane AS e
JOIN satis AS s ON s.eczane_no = e.eczane_no
GROUP BY e.eczane_no, e.ad
HAVING COUNT(s.satis_id) >= 2
   AND SUM(s.fiyat) > 200
ORDER BY toplam_ciro DESC;

-- S3 (c - Alt sorgu)
-- Soru: Ortalama satis fiyatinin uzerinde bir fiyata satilan ilaclarin satis kayitlari nelerdir?
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
WHERE s.fiyat > (
    SELECT AVG(fiyat)
    FROM satis
)
ORDER BY s.fiyat DESC;

-- S4 (d - LEFT JOIN)
-- Soru: Sistemdeki tum eczanelerin (hic satis yapmamis olanlar dahil) toplam satis sayisi ve toplam cirosu nedir?
SELECT
    e.eczane_no,
    e.ad AS eczane_ad,
    e.adres,
    COUNT(s.satis_id) AS satis_sayisi,
    COALESCE(SUM(s.fiyat), 0) AS toplam_ciro
FROM eczane AS e
LEFT JOIN satis AS s ON s.eczane_no = e.eczane_no
GROUP BY e.eczane_no, e.ad, e.adres
ORDER BY toplam_ciro DESC, e.eczane_no ASC;

-- S5 (e - NOT EXISTS)
-- Soru: Hic ilac satisi yapilmamis (satis kaydi bulunmayan) hastalar kimlerdir?
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas,
    h.adres
FROM hasta AS h
WHERE NOT EXISTS (
    SELECT 1
    FROM satis AS s
    WHERE s.hasta_kimlik_no = h.hasta_kimlik_no
)
ORDER BY h.ad ASC;

-- S6 (f - Tarih araligi + ORDER BY + LIMIT)
-- Soru: 2026 yili icinde yapilan en yuksek tutarli ilk 5 ilac satisi hangileridir?
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
WHERE s.satis_tarihi BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY s.fiyat DESC, s.satis_tarihi DESC
LIMIT 5;