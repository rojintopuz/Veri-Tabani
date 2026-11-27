-- ============================================================================
-- Dosya   : db/50_tetikleyiciler/m3_trg_satis_recete_kontrol.sql
-- Modul   : M3 Eczane & Satis
-- Sahibi  : Elifnur Ozkaya (032390036)
-- Aciklama: Is kurali: bir hastaya ilac satilabilmesi icin o hasta ve ilac
--           adina satis tarihinde veya oncesinde yazilmis bir recete kaydi
--           bulunmalidir.
-- ============================================================================

CREATE OR REPLACE FUNCTION trgf_satis_recete_kontrol()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM recete AS r
        WHERE r.hasta_kimlik_no = NEW.hasta_kimlik_no
          AND r.ilac_no = NEW.ilac_no
          AND r.recete_tarihi <= NEW.satis_tarihi
    ) THEN
        RAISE EXCEPTION 'Hasta (%) icin % numarali ilaca ait % tarihinde veya oncesinde yazilmis recete bulunamadi.',
            NEW.hasta_kimlik_no, NEW.ilac_no, NEW.satis_tarihi
            USING HINT = 'Ilac satisi yapmadan once gecerli bir recete kaydi olusturun.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_satis_recete_kontrol
BEFORE INSERT OR UPDATE OF hasta_kimlik_no, ilac_no, satis_tarihi ON satis
FOR EACH ROW
EXECUTE FUNCTION trgf_satis_recete_kontrol();