"""M4 Ilac & Tedarik modulunun SQL metinleri."""

# --- ILAC ---

ILAC_LISTELE = """
SELECT ilac_no, ticari_ad, formul
FROM ilac
ORDER BY ilac_no;
"""

ILAC_GETIR = """
SELECT ilac_no, ticari_ad, formul
FROM ilac
WHERE ilac_no = %(ilac_no)s;
"""

ILAC_EKLE = """
INSERT INTO ilac (ticari_ad, formul)
VALUES (%(ticari_ad)s, %(formul)s);
"""

ILAC_GUNCELLE = """
UPDATE ilac
SET ticari_ad = %(ticari_ad)s,
    formul = %(formul)s
WHERE ilac_no = %(ilac_no)s;
"""

ILAC_SIL = """
DELETE FROM ilac
WHERE ilac_no = %(ilac_no)s;
"""

# --- TEDARIKCI ---

TEDARIKCI_LISTELE = """
SELECT tedarikci_no, ad, adres
FROM tedarikci
ORDER BY tedarikci_no;
"""

TEDARIKCI_GETIR = """
SELECT tedarikci_no, ad, adres
FROM tedarikci
WHERE tedarikci_no = %(tedarikci_no)s;
"""

TEDARIKCI_EKLE = """
INSERT INTO tedarikci (ad, adres)
VALUES (%(ad)s, %(adres)s);
"""

TEDARIKCI_GUNCELLE = """
UPDATE tedarikci
SET ad = %(ad)s,
    adres = %(adres)s
WHERE tedarikci_no = %(tedarikci_no)s;
"""

TEDARIKCI_SIL = """
DELETE FROM tedarikci
WHERE tedarikci_no = %(tedarikci_no)s;
"""

# --- TEDARIK ---

TEDARIK_LISTELE = """
SELECT
    t.tedarik_id,
    t.tedarikci_no,
    tc.ad AS tedarikci_ad,
    t.eczane_no,
    e.ad AS eczane_ad,
    t.ilac_no,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN eczane AS e ON e.eczane_no = t.eczane_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
ORDER BY t.tedarik_tarihi DESC, t.tedarik_id DESC;
"""

TEDARIK_GETIR = """
SELECT tedarik_id, tedarikci_no, eczane_no, ilac_no, miktar, tedarik_tarihi
FROM tedarik
WHERE tedarik_id = %(tedarik_id)s;
"""

TEDARIK_EKLE = """
INSERT INTO tedarik (tedarikci_no, eczane_no, ilac_no, miktar, tedarik_tarihi)
VALUES (%(tedarikci_no)s, %(eczane_no)s, %(ilac_no)s, %(miktar)s, %(tedarik_tarihi)s);
"""

TEDARIK_GUNCELLE = """
UPDATE tedarik
SET tedarikci_no = %(tedarikci_no)s,
    eczane_no = %(eczane_no)s,
    ilac_no = %(ilac_no)s,
    miktar = %(miktar)s,
    tedarik_tarihi = %(tedarik_tarihi)s
WHERE tedarik_id = %(tedarik_id)s;
"""

TEDARIK_SIL = """
DELETE FROM tedarik
WHERE tedarik_id = %(tedarik_id)s;
"""

# Tedarik formundaki eczane secim listesi icin (eczane tablosu M3'e ait, sadece okunur).
ECZANE_SECENEKLERI = """
SELECT eczane_no, ad
FROM eczane
ORDER BY ad;
"""

# --- RAPOR (view, fonksiyon ve trigger'in sonuclari) ---

ILAC_TEDARIK_OZETI = """
SELECT
    ilac_no,
    ticari_ad,
    tedarik_sayisi,
    toplam_miktar,
    tedarikci_sayisi,
    eczane_sayisi,
    ilk_tedarik_tarihi,
    son_tedarik_tarihi
FROM vw_ilac_tedarik_ozeti
ORDER BY toplam_miktar DESC, ilac_no;
"""

ECZANE_ILAC_STOK = """
SELECT fn_eczane_ilac_stok(%(eczane_no)s, %(ilac_no)s) AS stok;
"""

TEDARIK_DENETIM_SON_KAYITLAR = """
SELECT denetim_id, tedarik_id, islem_turu, eski_miktar, yeni_miktar, islem_zamani
FROM tedarik_denetim
ORDER BY denetim_id DESC
LIMIT 15;
"""

# --- 6 IS SORGUSU (db/sorgular/m4_ilac_tedarik.sql ile ayni) ---

S1_UC_TABLOLU_JOIN = """
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    e.ad AS eczane_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN eczane AS e ON e.eczane_no = t.eczane_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
ORDER BY t.tedarik_tarihi DESC, t.tedarik_id DESC;
"""

S2_GROUP_BY_HAVING = """
SELECT
    tc.tedarikci_no,
    tc.ad AS tedarikci_ad,
    COUNT(t.tedarik_id) AS tedarik_sayisi,
    SUM(t.miktar) AS toplam_miktar
FROM tedarikci AS tc
JOIN tedarik AS t ON t.tedarikci_no = tc.tedarikci_no
GROUP BY tc.tedarikci_no, tc.ad
HAVING COUNT(t.tedarik_id) >= 3
   AND SUM(t.miktar) > 300
ORDER BY toplam_miktar DESC;
"""

S3_ALT_SORGU = """
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
WHERE t.miktar > (
    SELECT AVG(miktar)
    FROM tedarik
)
ORDER BY t.miktar DESC;
"""

S4_LEFT_JOIN = """
SELECT
    i.ilac_no,
    i.ticari_ad,
    COUNT(t.tedarik_id) AS tedarik_sayisi,
    COALESCE(SUM(t.miktar), 0) AS toplam_miktar
FROM ilac AS i
LEFT JOIN tedarik AS t ON t.ilac_no = i.ilac_no
GROUP BY i.ilac_no, i.ticari_ad
ORDER BY toplam_miktar DESC, i.ilac_no ASC;
"""

S5_NOT_EXISTS = """
SELECT
    tc.tedarikci_no,
    tc.ad AS tedarikci_ad,
    tc.adres
FROM tedarikci AS tc
WHERE NOT EXISTS (
    SELECT 1
    FROM tedarik AS t
    WHERE t.tedarikci_no = tc.tedarikci_no
)
ORDER BY tc.ad ASC;
"""

S6_TARIH_ARALIGI_LIMIT = """
SELECT
    t.tedarik_id,
    tc.ad AS tedarikci_ad,
    e.ad AS eczane_ad,
    i.ticari_ad,
    t.miktar,
    t.tedarik_tarihi
FROM tedarik AS t
JOIN tedarikci AS tc ON tc.tedarikci_no = t.tedarikci_no
JOIN eczane AS e ON e.eczane_no = t.eczane_no
JOIN ilac AS i ON i.ilac_no = t.ilac_no
WHERE t.tedarik_tarihi BETWEEN '2026-08-01' AND '2026-08-31'
ORDER BY t.miktar DESC, t.tedarik_tarihi ASC
LIMIT 5;
"""

SORGU_LISTESI = [
    {
        "kod": "S1",
        "tur": "a - 3 tablolu JOIN",
        "soru": "Her tedarik işleminde hangi tedarikçi hangi eczaneye hangi ilaçtan "
                "ne kadar ve ne zaman getirmiş?",
        "sql": S1_UC_TABLOLU_JOIN,
    },
    {
        "kod": "S2",
        "tur": "b - GROUP BY + HAVING",
        "soru": "En az 3 tedarik işlemi yapmış ve toplam 300 kutudan fazla ilaç getirmiş "
                "tedarikçiler hangileri?",
        "sql": S2_GROUP_BY_HAVING,
    },
    {
        "kod": "S3",
        "tur": "c - Alt sorgu",
        "soru": "Ortalama tedarik miktarının üzerinde getirilen tedarik işlemleri hangileri?",
        "sql": S3_ALT_SORGU,
    },
    {
        "kod": "S4",
        "tur": "d - LEFT JOIN",
        "soru": "Sistemdeki tüm ilaçlar (hiç tedarik edilmemiş olanlar dahil) toplam kaç kutu "
                "tedarik edilmiş?",
        "sql": S4_LEFT_JOIN,
    },
    {
        "kod": "S5",
        "tur": "e - NOT EXISTS",
        "soru": "Hiç tedarik işlemi yapmamış tedarikçiler hangileri?",
        "sql": S5_NOT_EXISTS,
    },
    {
        "kod": "S6",
        "tur": "f - Tarih aralığı + ORDER BY + LIMIT",
        "soru": "Ağustos 2026'da yapılan en büyük miktarlı ilk 5 tedarik işlemi hangileri?",
        "sql": S6_TARIH_ARALIGI_LIMIT,
    },
]
