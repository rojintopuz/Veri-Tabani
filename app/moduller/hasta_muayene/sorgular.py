"""M1 - Hasta & Muayene modulunun SQL metinleri."""

# --- HASTA ---

HASTA_LISTELE = """
    SELECT hasta_kimlik_no, ad, adres, yas
    FROM hasta
    ORDER BY ad;
"""

HASTA_GETIR = """
    SELECT hasta_kimlik_no, ad, adres, yas
    FROM hasta
    WHERE hasta_kimlik_no = %(hasta_kimlik_no)s;
"""

HASTA_EKLE = """
    INSERT INTO hasta (hasta_kimlik_no, ad, adres, yas)
    VALUES (%(hasta_kimlik_no)s, %(ad)s, %(adres)s, %(yas)s);
"""

HASTA_GUNCELLE = """
    UPDATE hasta
    SET ad = %(ad)s,
        adres = %(adres)s,
        yas = %(yas)s
    WHERE hasta_kimlik_no = %(hasta_kimlik_no)s;
"""

HASTA_SIL = """
    DELETE FROM hasta
    WHERE hasta_kimlik_no = %(hasta_kimlik_no)s;
"""

# --- MUAYENE ---

MUAYENE_LISTELE = """
    SELECT
        m.muayene_id,
        m.muayene_tarihi,
        m.hasta_kimlik_no,
        h.ad AS hasta_ad,
        m.doktor_no,
        d.ad AS doktor_ad,
        d.uzmanlik_alani
    FROM muayene AS m
    JOIN hasta  AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
    JOIN doktor AS d ON d.doktor_no = m.doktor_no
    ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC;
"""

MUAYENE_GETIR = """
    SELECT muayene_id, doktor_no, hasta_kimlik_no, muayene_tarihi
    FROM muayene
    WHERE muayene_id = %(muayene_id)s;
"""

MUAYENE_EKLE = """
    INSERT INTO muayene (doktor_no, hasta_kimlik_no, muayene_tarihi)
    VALUES (%(doktor_no)s, %(hasta_kimlik_no)s, %(muayene_tarihi)s);
"""

MUAYENE_GUNCELLE = """
    UPDATE muayene
    SET doktor_no = %(doktor_no)s,
        hasta_kimlik_no = %(hasta_kimlik_no)s,
        muayene_tarihi = %(muayene_tarihi)s
    WHERE muayene_id = %(muayene_id)s;
"""

MUAYENE_SIL = """
    DELETE FROM muayene
    WHERE muayene_id = %(muayene_id)s;
"""

# --- Form secenekleri ---

HASTA_SECENEKLERI = """
    SELECT hasta_kimlik_no, ad
    FROM hasta
    ORDER BY ad;
"""

DOKTOR_SECENEKLERI = """
    SELECT doktor_no, ad, uzmanlik_alani
    FROM doktor
    ORDER BY ad;
"""

# --- Rapor (view + fonksiyon) ---

HASTA_MUAYENE_OZETI = """
    SELECT
        hasta_kimlik_no,
        hasta_ad,
        yas,
        muayene_sayisi,
        farkli_doktor_sayisi,
        ilk_muayene_tarihi,
        son_muayene_tarihi
    FROM vw_hasta_muayene_ozeti
    ORDER BY muayene_sayisi DESC, hasta_ad;
"""

HASTA_MUAYENE_GECMISI = """
    SELECT muayene_id, muayene_tarihi, doktor_no, doktor_ad, uzmanlik_alani
    FROM fn_hasta_muayene_gecmisi(%(hasta_kimlik_no)s);
"""

# --- 6 is sorgusu (db/sorgular/m1_hasta_muayene.sql ile ayni) ---

S1_MUAYENE_DETAY = """
SELECT
    m.muayene_id,
    m.muayene_tarihi,
    h.ad AS hasta_ad,
    h.yas,
    d.ad AS doktor_ad,
    d.uzmanlik_alani
FROM muayene AS m
JOIN hasta  AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
JOIN doktor AS d ON d.doktor_no = m.doktor_no
ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC;
"""

S2_COK_DOKTORA_GIDEN_HASTALAR = """
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    COUNT(m.muayene_id)         AS muayene_sayisi,
    COUNT(DISTINCT m.doktor_no) AS farkli_doktor_sayisi
FROM hasta AS h
JOIN muayene AS m ON m.hasta_kimlik_no = h.hasta_kimlik_no
GROUP BY h.hasta_kimlik_no, h.ad
HAVING COUNT(DISTINCT m.doktor_no) >= 2
ORDER BY farkli_doktor_sayisi DESC, muayene_sayisi DESC, h.ad;
"""

S3_ORTALAMA_USTU_YASTAKI_HASTALAR = """
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas
FROM hasta AS h
WHERE h.yas > (
    SELECT AVG(h2.yas)
    FROM hasta AS h2
    WHERE h2.hasta_kimlik_no IN (
        SELECT m.hasta_kimlik_no
        FROM muayene AS m
    )
)
ORDER BY h.yas DESC;
"""

S4_DOKTOR_MUAYENE_SAYILARI = """
SELECT
    d.doktor_no,
    d.ad AS doktor_ad,
    d.uzmanlik_alani,
    COUNT(m.muayene_id)                 AS muayene_sayisi,
    COUNT(DISTINCT m.hasta_kimlik_no)   AS farkli_hasta_sayisi
FROM doktor AS d
LEFT JOIN muayene AS m ON m.doktor_no = d.doktor_no
GROUP BY d.doktor_no, d.ad, d.uzmanlik_alani
ORDER BY muayene_sayisi DESC, d.doktor_no;
"""

S5_MUAYENESIZ_HASTALAR = """
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas,
    h.adres
FROM hasta AS h
WHERE NOT EXISTS (
    SELECT 1
    FROM muayene AS m
    WHERE m.hasta_kimlik_no = h.hasta_kimlik_no
)
ORDER BY h.ad;
"""

S6_EKIM_SON_MUAYENELER = """
SELECT
    m.muayene_id,
    m.muayene_tarihi,
    h.ad AS hasta_ad,
    d.ad AS doktor_ad
FROM muayene AS m
JOIN hasta  AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
JOIN doktor AS d ON d.doktor_no = m.doktor_no
WHERE m.muayene_tarihi BETWEEN '2026-10-01' AND '2026-10-31'
ORDER BY m.muayene_tarihi DESC, m.muayene_id DESC
LIMIT 5;
"""

IS_SORGULARI = [
    ("S1", "Çok tablolu JOIN",
     "Her muayenede hangi hasta, hangi uzmanlıktaki hangi doktora, ne zaman muayene olmuştur?",
     S1_MUAYENE_DETAY),
    ("S2", "GROUP BY + HAVING",
     "En az 2 farklı doktora muayene olmuş hastalar kimlerdir ve kaç muayeneleri vardır?",
     S2_COK_DOKTORA_GIDEN_HASTALAR),
    ("S3", "Alt sorgu",
     "Yaşı, muayene olmuş hastaların ortalama yaşından büyük olan hastalar kimlerdir?",
     S3_ORTALAMA_USTU_YASTAKI_HASTALAR),
    ("S4", "LEFT JOIN",
     "Tüm doktorlar (hiç muayene yapmamış olanlar dahil) kaç muayene yapmış ve kaç farklı "
     "hasta görmüştür?",
     S4_DOKTOR_MUAYENE_SAYILARI),
    ("S5", "NOT EXISTS",
     "Sisteme kayıtlı olup hiç muayene olmamış hastalar kimlerdir?",
     S5_MUAYENESIZ_HASTALAR),
    ("S6", "Tarih aralığı + ORDER BY + LIMIT",
     "Ekim 2026'da yapılan muayenelerden en son tarihli 5 tanesi hangileridir?",
     S6_EKIM_SON_MUAYENELER),
]
