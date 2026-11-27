-- ============================================================
-- Dosya   : db/40_fonksiyonlar/m2_fn_doktor_en_cok_yazdigi_ilac.sql
-- Modul   : M2 Doktor & Recete
-- Sahibi  : Meltem Can (032490033)
-- Aciklama: Verilen doktorun en cok recete ettigi ilaci dondurur.
--           Siralama: recete sayisi, esitlikte toplam miktar, sonra
--           ilac_no. Doktor yoksa anlasilir bir hata verir; doktor
--           hic recete yazmadiysa bos sonuc doner.
-- Kullanim: SELECT * FROM fn_doktor_en_cok_yazdigi_ilac(1);
-- ============================================================

CREATE OR REPLACE FUNCTION fn_doktor_en_cok_yazdigi_ilac(p_doktor_no INTEGER)
RETURNS TABLE (
    ilac_no        INTEGER,
    ticari_ad      VARCHAR(100),
    recete_sayisi  BIGINT,
    toplam_miktar  BIGINT
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM doktor AS d
        WHERE d.doktor_no = p_doktor_no
    ) THEN
        RAISE EXCEPTION 'Doktor bulunamadi: %', p_doktor_no;
    END IF;

    RETURN QUERY
    SELECT
        i.ilac_no,
        i.ticari_ad,
        COUNT(r.recete_id)  AS recete_sayisi,
        SUM(r.miktar)       AS toplam_miktar
    FROM recete AS r
    JOIN ilac   AS i ON i.ilac_no = r.ilac_no
    WHERE r.doktor_no = p_doktor_no
    GROUP BY i.ilac_no, i.ticari_ad
    ORDER BY COUNT(r.recete_id) DESC, SUM(r.miktar) DESC, i.ilac_no
    LIMIT 1;
END;
$$;
