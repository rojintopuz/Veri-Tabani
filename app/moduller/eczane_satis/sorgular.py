"""M3 Eczane & Satis modulunun SQL metinleri."""

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