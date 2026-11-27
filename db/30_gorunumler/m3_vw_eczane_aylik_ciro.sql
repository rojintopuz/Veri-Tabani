-- ============================================================================
-- Dosya   : db/30_gorunumler/m3_vw_eczane_aylik_ciro.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Eczane ve ay bazinda toplam satis sayisi, toplam ciro ve ortalama
--           satis tutarini gosteren gorunum.
-- ============================================================================

CREATE OR REPLACE VIEW vw_eczane_aylik_ciro AS
SELECT
    e.eczane_no,
    e.ad                                AS eczane_ad,
    TO_CHAR(s.satis_tarihi, 'YYYY-MM')  AS ay,
    COUNT(s.satis_id)                   AS satis_sayisi,
    SUM(s.fiyat)                        AS toplam_ciro,
    ROUND(AVG(s.fiyat), 2)              AS ortalama_fiyat
FROM eczane AS e
JOIN satis  AS s ON s.eczane_no = e.eczane_no
GROUP BY e.eczane_no, e.ad, TO_CHAR(s.satis_tarihi, 'YYYY-MM');