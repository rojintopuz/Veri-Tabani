-- ============================================================================
-- Dosya   : db/30_gorunumler/m1_vw_hasta_muayene_ozeti.sql
-- Modul   : M1 Hasta & Muayene
-- Sahibi  : Rojin Topuz (032390078)
-- Aciklama: Her hasta icin muayene sayisi, gittigi farkli doktor sayisi,
--           ilk ve son muayene tarihi. Hic muayene olmayan hastalar da
--           listelenir (LEFT JOIN, sayilar 0, tarihler NULL).
-- ============================================================================

CREATE OR REPLACE VIEW vw_hasta_muayene_ozeti AS
SELECT
    h.hasta_kimlik_no,
    h.ad                          AS hasta_ad,
    h.yas,
    COUNT(m.muayene_id)           AS muayene_sayisi,
    COUNT(DISTINCT m.doktor_no)   AS farkli_doktor_sayisi,
    MIN(m.muayene_tarihi)         AS ilk_muayene_tarihi,
    MAX(m.muayene_tarihi)         AS son_muayene_tarihi
FROM hasta AS h
LEFT JOIN muayene AS m ON m.hasta_kimlik_no = h.hasta_kimlik_no
GROUP BY h.hasta_kimlik_no, h.ad, h.yas;
