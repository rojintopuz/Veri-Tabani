"""M3 Eczane & Satis modulunun SQL metinleri."""

# --- ECZANE CRUD ---

ECZANE_LISTELE = """
SELECT eczane_no, ad, adres
FROM eczane
ORDER BY eczane_no;
"""

ECZANE_GETIR = """
SELECT eczane_no, ad, adres
FROM eczane
WHERE eczane_no = %(eczane_no)s;
"""

ECZANE_EKLE = """
INSERT INTO eczane (ad, adres)
VALUES (%(ad)s, %(adres)s);
"""

ECZANE_GUNCELLE = """
UPDATE eczane
SET ad = %(ad)s,
    adres = %(adres)s
WHERE eczane_no = %(eczane_no)s;
"""

ECZANE_SIL = """
DELETE FROM eczane
WHERE eczane_no = %(eczane_no)s;
"""

# --- ECZANE TELEFON CRUD ---

TELEFON_LISTELE = """
SELECT et.eczane_no, e.ad AS eczane_ad, et.telefon_no
FROM eczane_telefon AS et
JOIN eczane AS e ON e.eczane_no = et.eczane_no
ORDER BY et.eczane_no, et.telefon_no;
"""

TELEFON_GETIR = """
SELECT eczane_no, telefon_no
FROM eczane_telefon
WHERE eczane_no = %(eczane_no)s
  AND telefon_no = %(telefon_no)s;
"""

TELEFON_EKLE = """
INSERT INTO eczane_telefon (eczane_no, telefon_no)
VALUES (%(eczane_no)s, %(telefon_no)s);
"""

TELEFON_GUNCELLE = """
UPDATE eczane_telefon
SET eczane_no = %(yeni_eczane_no)s,
    telefon_no = %(yeni_telefon_no)s
WHERE eczane_no = %(eski_eczane_no)s
  AND telefon_no = %(eski_telefon_no)s;
"""

TELEFON_SIL = """
DELETE FROM eczane_telefon
WHERE eczane_no = %(eczane_no)s
  AND telefon_no = %(telefon_no)s;
"""

# --- SATIS CRUD ---

SATIS_LISTELE = """
SELECT
    s.satis_id,
    s.satis_tarihi,
    s.eczane_no,
    e.ad AS eczane_ad,
    s.hasta_kimlik_no,
    h.ad AS hasta_ad,
    s.ilac_no,
    i.ticari_ad,
    s.fiyat
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN hasta  AS h ON h.hasta_kimlik_no = s.hasta_kimlik_no
JOIN ilac   AS i ON i.ilac_no = s.ilac_no
ORDER BY s.satis_tarihi DESC, s.satis_id DESC;
"""

SATIS_GETIR = """
SELECT satis_id, eczane_no, hasta_kimlik_no, ilac_no, fiyat, satis_tarihi
FROM satis
WHERE satis_id = %(satis_id)s;
"""

SATIS_EKLE = """
INSERT INTO satis (eczane_no, hasta_kimlik_no, ilac_no, fiyat, satis_tarihi)
VALUES (%(eczane_no)s, %(hasta_kimlik_no)s, %(ilac_no)s, %(fiyat)s, %(satis_tarihi)s);
"""

SATIS_GUNCELLE = """
UPDATE satis
SET eczane_no = %(eczane_no)s,
    hasta_kimlik_no = %(hasta_kimlik_no)s,
    ilac_no = %(ilac_no)s,
    fiyat = %(fiyat)s,
    satis_tarihi = %(satis_tarihi)s
WHERE satis_id = %(satis_id)s;
"""

SATIS_SIL = """
DELETE FROM satis
WHERE satis_id = %(satis_id)s;
"""

# --- Satis formundaki secim listeleri ---

ECZANE_SECENEKLERI = """
SELECT eczane_no, ad
FROM eczane
ORDER BY ad;
"""

HASTA_SECENEKLERI = """
SELECT hasta_kimlik_no, ad
FROM hasta
ORDER BY ad;
"""

ILAC_SECENEKLERI = """
SELECT ilac_no, ticari_ad
FROM ilac
ORDER BY ticari_ad;
"""

# --- 6 IS SORGUSU (db/sorgular/m3_eczane_satis.sql ile ayni) ---

S1_SATIS_DETAY = """
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    h.ad AS hasta_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN hasta AS h ON h.hasta_kimlik_no = s.hasta_kimlik_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
ORDER BY s.satis_tarihi DESC, s.satis_id DESC;
"""

S2_COK_SATIS_YAPAN_ECZANELER = """
SELECT
    e.eczane_no,
    e.ad AS eczane_ad,
    COUNT(s.satis_id) AS satis_sayisi,
    SUM(s.fiyat) AS toplam_ciro
FROM eczane AS e
JOIN satis AS s ON s.eczane_no = e.eczane_no
GROUP BY e.eczane_no, e.ad
HAVING COUNT(s.satis_id) >= 2
   AND SUM(s.fiyat) > 200
ORDER BY toplam_ciro DESC;
"""

S3_ORTALAMA_USTU_SATISLAR = """
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
WHERE s.fiyat > (
    SELECT AVG(fiyat)
    FROM satis
)
ORDER BY s.fiyat DESC;
"""

S4_ECZANE_SATIS_OZETI = """
SELECT
    e.eczane_no,
    e.ad AS eczane_ad,
    e.adres,
    COUNT(s.satis_id) AS satis_sayisi,
    COALESCE(SUM(s.fiyat), 0) AS toplam_ciro
FROM eczane AS e
LEFT JOIN satis AS s ON s.eczane_no = e.eczane_no
GROUP BY e.eczane_no, e.ad, e.adres
ORDER BY toplam_ciro DESC, e.eczane_no ASC;
"""

S5_SATIS_YAPILMAYAN_HASTALAR = """
SELECT
    h.hasta_kimlik_no,
    h.ad AS hasta_ad,
    h.yas,
    h.adres
FROM hasta AS h
WHERE NOT EXISTS (
    SELECT 1
    FROM satis AS s
    WHERE s.hasta_kimlik_no = h.hasta_kimlik_no
)
ORDER BY h.ad ASC;
"""

S6_2026_EN_YUKSEK_SATISLAR = """
SELECT
    s.satis_id,
    e.ad AS eczane_ad,
    i.ticari_ad,
    s.fiyat,
    s.satis_tarihi
FROM satis AS s
JOIN eczane AS e ON e.eczane_no = s.eczane_no
JOIN ilac AS i ON i.ilac_no = s.ilac_no
WHERE s.satis_tarihi BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY s.fiyat DESC, s.satis_tarihi DESC
LIMIT 5;
"""

IS_SORGULARI = [
    ("S1", "Çok tablolu JOIN",
     "Her satışta hangi eczane hangi hastaya hangi ilacı kaç liraya ve ne zaman satmıştır?",
     S1_SATIS_DETAY),
    ("S2", "GROUP BY + HAVING",
     "En az 2 satış yapmış ve toplam cirosu 200 TL üzerinde olan eczanelerin satış sayısı "
     "ve toplam cirosu nedir?",
     S2_COK_SATIS_YAPAN_ECZANELER),
    ("S3", "Alt sorgu",
     "Ortalama satış fiyatının üzerinde bir fiyata satılan ilaçların satış kayıtları nelerdir?",
     S3_ORTALAMA_USTU_SATISLAR),
    ("S4", "LEFT JOIN",
     "Sistemdeki tüm eczanelerin (hiç satış yapmamış olanlar dahil) toplam satış sayısı ve "
     "toplam cirosu nedir?",
     S4_ECZANE_SATIS_OZETI),
    ("S5", "NOT EXISTS",
     "Hiç ilaç satışı yapılmamış (satış kaydı bulunmayan) hastalar kimlerdir?",
     S5_SATIS_YAPILMAYAN_HASTALAR),
    ("S6", "Tarih aralığı + ORDER BY + LIMIT",
     "2026 yılı içinde yapılan en yüksek tutarlı ilk 5 ilaç satışı hangileridir?",
     S6_2026_EN_YUKSEK_SATISLAR),
]

# --- RAPOR (VIEW ve FUNCTION) ---

AYLIK_CIRO_LISTELE = """
SELECT eczane_no, eczane_ad, ay, satis_sayisi, toplam_ciro, ortalama_fiyat
FROM vw_eczane_aylik_ciro
ORDER BY ay DESC, toplam_ciro DESC, eczane_no ASC;
"""

ECZANE_CIRO_HESAPLA = """
SELECT fn_eczane_ciro(%(eczane_no)s, %(baslangic)s, %(bitis)s) AS toplam_ciro;
"""