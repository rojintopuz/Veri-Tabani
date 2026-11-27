-- ============================================================================
-- Dosya   : db/40_fonksiyonlar/m4_fn_eczane_ilac_stok.sql
-- Modul   : M4 Ilac & Tedarik
-- Sahibi  : Altyn Baktybekova (032390093)
-- Aciklama: Bir eczanedeki bir ilacin hesaplanan stogunu dondurur:
--           stok = toplam tedarik miktari - satis sayisi
--           (Varsayim 3: her satis kaydi 1 kutudur.)
--           Eczane veya ilac yoksa anlasilir bir hata verir.
-- Kullanim: SELECT fn_eczane_ilac_stok(1, 1);
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_eczane_ilac_stok(
    p_eczane_no INTEGER,
    p_ilac_no   INTEGER
)
RETURNS INTEGER
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_toplam_tedarik INTEGER;
    v_satis_sayisi   INTEGER;
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM eczane AS e
        WHERE e.eczane_no = p_eczane_no
    ) THEN
        RAISE EXCEPTION 'Eczane bulunamadı: %', p_eczane_no;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM ilac AS i
        WHERE i.ilac_no = p_ilac_no
    ) THEN
        RAISE EXCEPTION 'İlaç bulunamadı: %', p_ilac_no;
    END IF;

    SELECT COALESCE(SUM(t.miktar), 0)
    INTO v_toplam_tedarik
    FROM tedarik AS t
    WHERE t.eczane_no = p_eczane_no
      AND t.ilac_no = p_ilac_no;

    SELECT COUNT(*)
    INTO v_satis_sayisi
    FROM satis AS s
    WHERE s.eczane_no = p_eczane_no
      AND s.ilac_no = p_ilac_no;

    RETURN v_toplam_tedarik - v_satis_sayisi;
END;
$$;
