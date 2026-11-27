-- ============================================================================
-- Dosya   : db/30_gorunumler/m4_vw_ilac_tedarik_ozeti.sql
-- Modul   : M4 Ilac & Tedarik
-- Sahibi  : Altyn Baktybekova (032390093)
-- Aciklama: Her ilac icin tedarik islemi sayisi, toplam tedarik miktari,
--           kac farkli tedarikciden ve kac farkli eczaneye geldigi, ilk ve son
--           tedarik tarihi. Hic tedarik edilmemis ilaclar da listelenir
--           (LEFT JOIN, sayilar 0, tarihler NULL).
-- ============================================================================

CREATE OR REPLACE VIEW vw_ilac_tedarik_ozeti AS
SELECT
    i.ilac_no,
    i.ticari_ad,
    COUNT(t.tedarik_id)                 AS tedarik_sayisi,
    COALESCE(SUM(t.miktar), 0)          AS toplam_miktar,
    COUNT(DISTINCT t.tedarikci_no)      AS tedarikci_sayisi,
    COUNT(DISTINCT t.eczane_no)         AS eczane_sayisi,
    MIN(t.tedarik_tarihi)               AS ilk_tedarik_tarihi,
    MAX(t.tedarik_tarihi)               AS son_tedarik_tarihi
FROM ilac AS i
LEFT JOIN tedarik AS t ON t.ilac_no = i.ilac_no
GROUP BY i.ilac_no, i.ticari_ad;
