-- ============================================================
-- Dosya   : db/30_gorunumler/m2_vw_doktor_recete_istatistigi.sql
-- Modul   : M2 Doktor & Recete
-- Sahibi  : Meltem Can (032490033)
-- Aciklama: Her doktor icin recete sayisi, toplam recete edilen ilac
--           miktari, recete yazdigi farkli hasta ve ilac sayisi, ilk ve
--           son recete tarihi. Hic recete yazmamis doktorlar da
--           listelenir (LEFT JOIN, sayilar 0, tarihler NULL).
-- ============================================================

CREATE OR REPLACE VIEW vw_doktor_recete_istatistigi AS
SELECT
    d.doktor_no,
    d.ad                                AS doktor_ad,
    d.uzmanlik_alani,
    COUNT(r.recete_id)                  AS recete_sayisi,
    COALESCE(SUM(r.miktar), 0)          AS toplam_miktar,
    COUNT(DISTINCT r.hasta_kimlik_no)   AS farkli_hasta_sayisi,
    COUNT(DISTINCT r.ilac_no)           AS farkli_ilac_sayisi,
    MIN(r.recete_tarihi)                AS ilk_recete_tarihi,
    MAX(r.recete_tarihi)                AS son_recete_tarihi
FROM doktor AS d
LEFT JOIN recete AS r ON r.doktor_no = d.doktor_no
GROUP BY d.doktor_no, d.ad, d.uzmanlik_alani;
