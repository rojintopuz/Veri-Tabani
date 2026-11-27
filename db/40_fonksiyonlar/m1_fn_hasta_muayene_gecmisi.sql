-- ============================================================================
-- Dosya   : db/40_fonksiyonlar/m1_fn_hasta_muayene_gecmisi.sql
-- Modul   : M1 Hasta & Muayene
-- Sahibi  : Rojin Topuz (032390078)
-- Aciklama: Verilen hastanin tum muayenelerini, muayene eden doktorun adi ve
--           uzmanlik alaniyla birlikte en yeniden eskiye dondurur.
--           Hasta yoksa anlasilir bir hata verir.
-- Kullanim: SELECT * FROM fn_hasta_muayene_gecmisi('11345678922');
-- ============================================================================

CREATE OR REPLACE FUNCTION fn_hasta_muayene_gecmisi(p_hasta_kimlik_no CHAR(11))
RETURNS TABLE (
    muayene_id      INTEGER,
    muayene_tarihi  DATE,
    doktor_no       INTEGER,
    doktor_ad       VARCHAR(100),
    uzmanlik_alani  VARCHAR(100)
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM hasta AS h
        WHERE h.hasta_kimlik_no = p_hasta_kimlik_no
    ) THEN
        RAISE EXCEPTION 'Hasta bulunamadi: %', p_hasta_kimlik_no;
    END IF;

    RETURN QUERY
    SELECT
        m.muayene_id,
        m.muayene_tarihi,
        d.doktor_no,
        d.ad,
        d.uzmanlik_alani
    FROM muayene AS m
    JOIN doktor  AS d ON d.doktor_no = m.doktor_no
    WHERE m.hasta_kimlik_no = p_hasta_kimlik_no
    ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC;
END;
$$;
