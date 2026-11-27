-- ============================================================================
-- Dosya   : db/sorgular/m4_ilac_tedarik.sql
-- Modul   : M4 Ilac & Tedarik
-- Sahibi  : Altyn Baktybekova (032390093)
-- Aciklama: Ilac ve tedarik modulu icin 6 is sorgusu
-- ============================================================================

-- S1 (a - >=3 tablolu JOIN)
-- Soru: Her tedarik isleminde hangi tedarikci hangi eczaneye hangi ilactan ne kadar ve ne zaman getirmis?
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    e.ad AS eczane_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN eczane AS e ON e.eczane_no = t.eczane_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
ORDER BY t.tedarik_tarihi DESC, t.tedarik_id DESC;

-- S2 (b - GROUP BY + HAVING)
-- Soru: En az 3 tedarik islemi yapmis ve toplam 300 kutudan fazla ilac getirmis tedarikciler hangileri?
SELECT
    tc.tedarikci_no,
    tc.ad AS tedarikci_ad,
    COUNT(t.tedarik_id) AS tedarik_sayisi,
    SUM(t.miktar) AS toplam_miktar
FROM tedarikci AS tc
JOIN tedarik AS t ON t.tedarikci_no = tc.tedarikci_no
GROUP BY tc.tedarikci_no, tc.ad
HAVING COUNT(t.tedarik_id) >= 3
   AND SUM(t.miktar) > 300
ORDER BY toplam_miktar DESC;

-- S3 (c - Alt sorgu)
-- Soru: Ortalama tedarik miktarinin uzerinde getirilen tedarik islemleri hangileri?
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
WHERE t.miktar > (
    SELECT AVG(miktar)
    FROM tedarik
)
ORDER BY t.miktar DESC;

-- S4 (d - LEFT JOIN)
-- Soru: Sistemdeki tum ilaclar (hic tedarik edilmemis olanlar dahil) toplam kac kutu tedarik edilmis?
SELECT
    i.ilac_no,
    i.ticari_ad,
    COUNT(t.tedarik_id) AS tedarik_sayisi,
    COALESCE(SUM(t.miktar), 0) AS toplam_miktar
FROM ilac AS i
LEFT JOIN tedarik AS t ON t.ilac_no = i.ilac_no
GROUP BY i.ilac_no, i.ticari_ad
ORDER BY toplam_miktar DESC, i.ilac_no ASC;

-- S5 (e - NOT EXISTS)
-- Soru: Hic tedarik islemi yapmamis tedarikciler hangileri?
SELECT
    tc.tedarikci_no,
    tc.ad AS tedarikci_ad,
    tc.adres
FROM tedarikci AS tc
WHERE NOT EXISTS (
    SELECT 1
    FROM tedarik AS t
    WHERE t.tedarikci_no = tc.tedarikci_no
)
ORDER BY tc.ad ASC;

-- S6 (f - Tarih araligi + ORDER BY + LIMIT)
-- Soru: Agustos 2026'da yapilan en buyuk miktarli ilk 5 tedarik islemi hangileri?
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    e.ad AS eczane_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN eczane AS e ON e.eczane_no = t.eczane_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
WHERE t.tedarik_tarihi BETWEEN '2026-08-01' AND '2026-08-31'
ORDER BY t.miktar DESC, t.tedarik_tarihi ASC
LIMIT 5;
