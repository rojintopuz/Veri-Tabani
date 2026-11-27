-- ============================================================
-- Dosya   : db/sorgular/m2_doktor_recete.sql
-- Modul   : M2 Doktor & Recete
-- Sahibi  : Meltem Can (032490033)
-- Aciklama: Doktor ve recete modulu icin 6 is sorgusu
-- ============================================================

-- S1 (a - >=3 tablolu JOIN)
-- Soru: Her recetede hangi doktor, hangi hastaya, hangi ilactan ne kadar ve ne zaman yazmistir?
SELECT
    r.recete_id,
    r.recete_tarihi,
    d.ad AS doktor_ad,
    d.uzmanlik_alani,
    h.ad AS hasta_ad,
    i.ticari_ad,
    r.miktar
FROM recete AS r
JOIN doktor AS d ON d.doktor_no = r.doktor_no
JOIN hasta  AS h ON h.hasta_kimlik_no = r.hasta_kimlik_no
JOIN ilac   AS i ON i.ilac_no = r.ilac_no
ORDER BY r.recete_tarihi DESC, r.recete_id DESC;

-- S2 (b - GROUP BY + HAVING)
-- Soru: En az 3 recete yazmis doktorlar kimlerdir, kac recete ve toplam ne kadar ilac yazmislardir?
SELECT
    d.doktor_no,
    d.ad AS doktor_ad,
    d.uzmanlik_alani,
    COUNT(r.recete_id) AS recete_sayisi,
    SUM(r.miktar)      AS toplam_miktar
FROM doktor AS d
JOIN recete AS r ON r.doktor_no = d.doktor_no
GROUP BY d.doktor_no, d.ad, d.uzmanlik_alani
HAVING COUNT(r.recete_id) >= 3
ORDER BY recete_sayisi DESC, toplam_miktar DESC, d.doktor_no;

-- S3 (c - Alt sorgu)
-- Soru: Miktari, tum recetelerin ortalama miktarindan fazla olan receteler hangileridir?
SELECT
    r.recete_id,
    r.recete_tarihi,
    d.ad AS doktor_ad,
    i.ticari_ad,
    r.miktar
FROM recete AS r
JOIN doktor AS d ON d.doktor_no = r.doktor_no
JOIN ilac   AS i ON i.ilac_no = r.ilac_no
WHERE r.miktar > (
    SELECT AVG(r2.miktar)
    FROM recete AS r2
)
ORDER BY r.miktar DESC, r.recete_tarihi;

-- S4 (d - LEFT JOIN)
-- Soru: Tum ilaclar (hic recete edilmemis olanlar dahil) kac recetede ve toplam ne kadar yazilmistir?
SELECT
    i.ilac_no,
    i.ticari_ad,
    COUNT(r.recete_id)          AS recete_sayisi,
    COALESCE(SUM(r.miktar), 0)  AS toplam_miktar
FROM ilac AS i
LEFT JOIN recete AS r ON r.ilac_no = i.ilac_no
GROUP BY i.ilac_no, i.ticari_ad
ORDER BY recete_sayisi DESC, toplam_miktar DESC, i.ilac_no;

-- S5 (e - NOT EXISTS)
-- Soru: Hangi muayenelerin ardindan ayni doktor o hastaya hic recete yazmamistir?
SELECT
    m.muayene_id,
    m.muayene_tarihi,
    d.ad AS doktor_ad,
    h.ad AS hasta_ad
FROM muayene AS m
JOIN doktor  AS d ON d.doktor_no = m.doktor_no
JOIN hasta   AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
WHERE NOT EXISTS (
    SELECT 1
    FROM recete AS r
    WHERE r.doktor_no = m.doktor_no
      AND r.hasta_kimlik_no = m.hasta_kimlik_no
      AND r.recete_tarihi >= m.muayene_tarihi
)
ORDER BY m.muayene_tarihi DESC;

-- S6 (f - Tarih araligi + ORDER BY + LIMIT)
-- Soru: Ekim 2026'da yazilan recetelerden miktari en yuksek 5 tanesi hangileridir?
SELECT
    r.recete_id,
    r.recete_tarihi,
    d.ad AS doktor_ad,
    h.ad AS hasta_ad,
    i.ticari_ad,
    r.miktar
FROM recete AS r
JOIN doktor AS d ON d.doktor_no = r.doktor_no
JOIN hasta  AS h ON h.hasta_kimlik_no = r.hasta_kimlik_no
JOIN ilac   AS i ON i.ilac_no = r.ilac_no
WHERE r.recete_tarihi BETWEEN '2026-10-01' AND '2026-10-31'
ORDER BY r.miktar DESC, r.recete_tarihi DESC
LIMIT 5;
