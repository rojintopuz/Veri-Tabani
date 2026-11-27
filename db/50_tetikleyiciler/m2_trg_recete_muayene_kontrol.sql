-- ============================================================
-- Dosya   : db/50_tetikleyiciler/m2_trg_recete_muayene_kontrol.sql
-- Modul   : M2 Doktor & Recete
-- Sahibi  : Meltem Can (032490033)
-- Aciklama: Is kurali: doktor bir hastaya, o hastayi recete tarihinde
--           veya daha once muayene etmediyse recete yazamaz.
--           Gelecek tarihli recete de kaydedilemez.
--           INSERT ve ilgili kolonlarin UPDATE'i oncesi calisir; kural
--           ihlalinde islem iptal edilir.
-- ============================================================

CREATE OR REPLACE FUNCTION trgf_recete_muayene_kontrol()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.recete_tarihi > CURRENT_DATE THEN
        RAISE EXCEPTION 'Recete tarihi gelecekte olamaz: %', NEW.recete_tarihi
            USING HINT = 'Bugunun veya gecmis bir gunun tarihini girin.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM muayene AS m
        WHERE m.doktor_no = NEW.doktor_no
          AND m.hasta_kimlik_no = NEW.hasta_kimlik_no
          AND m.muayene_tarihi <= NEW.recete_tarihi
    ) THEN
        RAISE EXCEPTION 'Doktor % bu hastayi (%) % tarihinde veya oncesinde muayene etmemis.',
            NEW.doktor_no, NEW.hasta_kimlik_no, NEW.recete_tarihi
            USING HINT = 'Recete yazmadan once muayene kaydi girin.';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_recete_muayene_kontrol
BEFORE INSERT OR UPDATE OF doktor_no, hasta_kimlik_no, recete_tarihi ON recete
FOR EACH ROW
EXECUTE FUNCTION trgf_recete_muayene_kontrol();
