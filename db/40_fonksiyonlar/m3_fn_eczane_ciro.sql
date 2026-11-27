-- ============================================================================
-- Dosya   : db/40_fonksiyonlar/m3_fn_eczane_ciro.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Belirli bir eczanenin verilen tarih araligindaki toplam cirosunu
--           hesaplar. Eczane yoksa veya tarih araligi gecersizse hata verir;
--           aralikta satis yoksa 0.00 dondurur.
-- Kullanim: SELECT fn_eczane_ciro(1, '2026-01-01', '2026-12-31');
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_eczane_ciro(
    p_eczane_no INTEGER,
    p_baslangic DATE,
    p_bitis     DATE
)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_toplam_ciro NUMERIC(10,2);
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM eczane AS e
        WHERE e.eczane_no = p_eczane_no
    ) THEN
        RAISE EXCEPTION 'Eczane bulunamadi: %', p_eczane_no;
    END IF;

    IF p_baslangic > p_bitis THEN
        RAISE EXCEPTION 'Baslangic tarihi (%) bitis tarihinden (%) buyuk olamaz.',
            p_baslangic, p_bitis;
    END IF;

    SELECT COALESCE(SUM(s.fiyat), 0)::NUMERIC(10,2)
    INTO v_toplam_ciro
    FROM satis AS s
    WHERE s.eczane_no = p_eczane_no
      AND s.satis_tarihi BETWEEN p_baslangic AND p_bitis;

    RETURN v_toplam_ciro;
END;
$$;