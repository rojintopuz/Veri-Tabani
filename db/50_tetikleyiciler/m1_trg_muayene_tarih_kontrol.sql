-- ============================================================================
-- Dosya   : db/50_tetikleyiciler/m1_trg_muayene_tarih_kontrol.sql
-- Modul   : M1 Hasta & Muayene
-- Sahibi  : Rojin Topuz (032390078)
-- Aciklama: Is kurali: gelecek tarihli muayene kaydedilemez.
--           INSERT ve UPDATE oncesi calisir; kural ihlalinde islem iptal edilir.
-- ============================================================================

CREATE OR REPLACE FUNCTION trgf_muayene_tarih_kontrol()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.muayene_tarihi > CURRENT_DATE THEN
        RAISE EXCEPTION 'Muayene tarihi gelecekte olamaz: %', NEW.muayene_tarihi
            USING HINT = 'Bugunun veya gecmis bir gunun tarihini girin.';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_muayene_tarih_kontrol
BEFORE INSERT OR UPDATE OF muayene_tarihi ON muayene
FOR EACH ROW
EXECUTE FUNCTION trgf_muayene_tarih_kontrol();
