-- ============================================================================
-- Dosya   : db/sorgular/m1_hasta_muayene.sql
-- Modul   : M1 Hasta & Muayene
-- Sahibi  : Rojin Topuz (032390078)
-- Aciklama: Hasta ve muayene modulu icin 6 is sorgusu
-- ============================================================================

-- S1 (a - >=3 tablolu JOIN)
-- Soru: Her muayenede hangi hasta, hangi uzmanliktaki hangi doktora, ne zaman muayene olmustur?
SELECT
    m.muayene_id,
    m.muayene_tarihi,
    h.ad AS hasta_ad,
    h.yas,
    d.ad AS doktor_ad,
    d.uzmanlik_alani
FROM muayene AS m
JOIN hasta  AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
JOIN doktor AS d ON d.doktor_no = m.doktor_no
ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC;

-- S2 (b - GROUP BY + HAVING)
-- Soru: En az 2 farkli doktora muayene olmus hastalar kimlerdir ve kac muayeneleri vardir?
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    COUNT(m.muayene_id)         AS muayene_sayisi,
    COUNT(DISTINCT m.doktor_no) AS farkli_doktor_sayisi
FROM hasta AS h
JOIN muayene AS m ON m.hasta_kimlik_no = h.hasta_kimlik_no
GROUP BY h.hasta_kimlik_no, h.ad
HAVING COUNT(DISTINCT m.doktor_no) >= 2
ORDER BY farkli_doktor_sayisi DESC, muayene_sayisi DESC, h.ad;

-- S3 (c - Alt sorgu)
-- Soru: Yasi, muayene olmus hastalarin ortalama yasindan buyuk olan hastalar kimlerdir?
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas
FROM hasta AS h
WHERE h.yas > (
    SELECT AVG(h2.yas)
    FROM hasta AS h2
    WHERE h2.hasta_kimlik_no IN (
        SELECT m.hasta_kimlik_no
        FROM muayene AS m
    )
)
ORDER BY h.yas DESC;

-- S4 (d - LEFT JOIN)
-- Soru: Tum doktorlar (hic muayene yapmamis olanlar dahil) kac muayene yapmis ve kac farkli hasta gormustur?
SELECT
    d.doktor_no,
    d.ad AS doktor_ad,
    d.uzmanlik_alani,
    COUNT(m.muayene_id)                 AS muayene_sayisi,
    COUNT(DISTINCT m.hasta_kimlik_no)   AS farkli_hasta_sayisi
FROM doktor AS d
LEFT JOIN muayene AS m ON m.doktor_no = d.doktor_no
GROUP BY d.doktor_no, d.ad, d.uzmanlik_alani
ORDER BY muayene_sayisi DESC, d.doktor_no;

-- S5 (e - NOT EXISTS)
-- Soru: Sisteme kayitli olup hic muayene olmamis hastalar kimlerdir?
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas,
    h.adres
FROM hasta AS h
WHERE NOT EXISTS (
    SELECT 1
    FROM muayene AS m
    WHERE m.hasta_kimlik_no = h.hasta_kimlik_no
)
ORDER BY h.ad;

-- S6 (f - Tarih araligi + ORDER BY + LIMIT)
-- Soru: Ekim 2026'da yapilan muayenelerden en son tarihli 5 tanesi hangileridir?
SELECT
    m.muayene_id,
    m.muayene_tarihi,
    h.ad AS hasta_ad,
    d.ad AS doktor_ad
FROM muayene AS m
JOIN hasta  AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
JOIN doktor AS d ON d.doktor_no = m.doktor_no
WHERE m.muayene_tarihi BETWEEN '2026-10-01' AND '2026-10-31'
ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC
LIMIT 5;
