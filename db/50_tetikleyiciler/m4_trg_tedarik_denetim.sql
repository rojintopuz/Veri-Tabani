-- ============================================================================
-- Dosya   : db/50_tetikleyiciler/m4_trg_tedarik_denetim.sql
-- Modul   : M4 Ilac & Tedarik
-- Sahibi  : Altyn Baktybekova (032390093)
-- Aciklama: tedarik tablosundaki her ekleme, guncelleme ve silme islemini
--           tedarik_denetim tablosuna loglar (islem turu, eski ve yeni
--           miktar, islem zamani). Islem bittikten sonra (AFTER) calisir.
-- ============================================================================

CREATE OR REPLACE FUNCTION trgf_tedarik_denetim()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO tedarik_denetim (tedarik_id, islem_turu, eski_miktar, yeni_miktar)
        VALUES (NEW.tedarik_id, 'INSERT', NULL, NEW.miktar);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO tedarik_denetim (tedarik_id, islem_turu, eski_miktar, yeni_miktar)
        VALUES (NEW.tedarik_id, 'UPDATE', OLD.miktar, NEW.miktar);
        RETURN NEW;
    ELSE
        INSERT INTO tedarik_denetim (tedarik_id, islem_turu, eski_miktar, yeni_miktar)
        VALUES (OLD.tedarik_id, 'DELETE', OLD.miktar, NULL);
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_tedarik_denetim
AFTER INSERT OR UPDATE OR DELETE ON tedarik
FOR EACH ROW
EXECUTE FUNCTION trgf_tedarik_denetim();
