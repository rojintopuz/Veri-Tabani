"""M2 - Doktor & Recete modulunun SQL metinleri."""

# --- DOKTOR ---

DOKTOR_LISTELE = """
    SELECT doktor_no, ad, uzmanlik_alani, deneyim_yili
    FROM doktor
    ORDER BY doktor_no;
"""

DOKTOR_GETIR = """
    SELECT doktor_no, ad, uzmanlik_alani, deneyim_yili
    FROM doktor
    WHERE doktor_no = %(doktor_no)s;
"""

DOKTOR_EKLE = """
    INSERT INTO doktor (ad, uzmanlik_alani, deneyim_yili)
    VALUES (%(ad)s, %(uzmanlik_alani)s, %(deneyim_yili)s);
"""

DOKTOR_GUNCELLE = """
    UPDATE doktor
    SET ad = %(ad)s,
        uzmanlik_alani = %(uzmanlik_alani)s,
        deneyim_yili = %(deneyim_yili)s
    WHERE doktor_no = %(doktor_no)s;
"""

DOKTOR_SIL = """
    DELETE FROM doktor
    WHERE doktor_no = %(doktor_no)s;
"""

# --- RECETE ---

RECETE_LISTELE = """
    SELECT
        r.recete_id,
        r.recete_tarihi,
        r.doktor_no,
        d.ad AS doktor_ad,
        r.hasta_kimlik_no,
        h.ad AS hasta_ad,
        r.ilac_no,
        i.ticari_ad,
        r.miktar
    FROM recete AS r
    JOIN doktor AS d ON d.doktor_no = r.doktor_no
    JOIN hasta  AS h ON h.hasta_kimlik_no = r.hasta_kimlik_no
    JOIN ilac   AS i ON i.ilac_no = r.ilac_no
    ORDER BY r.recete_tarihi DESC, r.recete_id DESC;
"""

RECETE_GETIR = """
    SELECT recete_id, doktor_no, hasta_kimlik_no, ilac_no, recete_tarihi, miktar
    FROM recete
    WHERE recete_id = %(recete_id)s;
"""

RECETE_EKLE = """
    INSERT INTO recete (doktor_no, hasta_kimlik_no, ilac_no, recete_tarihi, miktar)
    VALUES (%(doktor_no)s, %(hasta_kimlik_no)s, %(ilac_no)s, %(recete_tarihi)s, %(miktar)s);
"""

RECETE_GUNCELLE = """
    UPDATE recete
    SET doktor_no = %(doktor_no)s,
        hasta_kimlik_no = %(hasta_kimlik_no)s,
        ilac_no = %(ilac_no)s,
        recete_tarihi = %(recete_tarihi)s,
        miktar = %(miktar)s
    WHERE recete_id = %(recete_id)s;
"""

RECETE_SIL = """
    DELETE FROM recete
    WHERE recete_id = %(recete_id)s;
"""

# --- Recete formundaki secim listeleri ---

DOKTOR_SECENEKLERI = """
    SELECT doktor_no, ad, uzmanlik_alani
    FROM doktor
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

# --- RAPOR (view + fonksiyon) ---

DOKTOR_RECETE_ISTATISTIGI = """
    SELECT
        doktor_no,
        doktor_ad,
        uzmanlik_alani,
        recete_sayisi,
        toplam_miktar,
        farkli_hasta_sayisi,
        farkli_ilac_sayisi,
        ilk_recete_tarihi,
        son_recete_tarihi
    FROM vw_doktor_recete_istatistigi
    ORDER BY recete_sayisi DESC, toplam_miktar DESC, doktor_no;
"""

DOKTOR_EN_COK_YAZDIGI_ILAC = """
    SELECT ilac_no, ticari_ad, recete_sayisi, toplam_miktar
    FROM fn_doktor_en_cok_yazdigi_ilac(%(doktor_no)s);
"""

# --- 6 IS SORGUSU (db/sorgular/m2_doktor_recete.sql ile ayni) ---

S1_RECETE_DETAY = """
    SELECT
        r.recete_id,
        r.recete_tarihi,
        d.ad AS doktor_ad,
        d.uzmanlik_alani,
        h.ad AS hasta_ad,
        i.ticari_ad,
        r.miktar
    FROM recete AS r
    JOIN doktor AS d ON d.doktor_no = r.doktor_no
    JOIN hasta  AS h ON h.hasta_kimlik_no = r.hasta_kimlik_no
    JOIN ilac   AS i ON i.ilac_no = r.ilac_no
    ORDER BY r.recete_tarihi DESC, r.recete_id DESC;
"""

S2_COK_RECETE_YAZAN_DOKTORLAR = """
    SELECT
        d.doktor_no,
        d.ad AS doktor_ad,
        d.uzmanlik_alani,
        COUNT(r.recete_id) AS recete_sayisi,
        SUM(r.miktar)      AS toplam_miktar
    FROM doktor AS d
    JOIN recete AS r ON r.doktor_no = d.doktor_no
    GROUP BY d.doktor_no, d.ad, d.uzmanlik_alani
    HAVING COUNT(r.recete_id) >= 3
    ORDER BY recete_sayisi DESC, toplam_miktar DESC, d.doktor_no;
"""

S3_ORTALAMA_USTU_RECETELER = """
    SELECT
        r.recete_id,
        r.recete_tarihi,
        d.ad AS doktor_ad,
        i.ticari_ad,
        r.miktar
    FROM recete AS r
    JOIN doktor AS d ON d.doktor_no = r.doktor_no
    JOIN ilac   AS i ON i.ilac_no = r.ilac_no
    WHERE r.miktar > (
        SELECT AVG(r2.miktar)
        FROM recete AS r2
    )
    ORDER BY r.miktar DESC, r.recete_tarihi;
"""

S4_ILAC_RECETE_SAYILARI = """
    SELECT
        i.ilac_no,
        i.ticari_ad,
        COUNT(r.recete_id)          AS recete_sayisi,
        COALESCE(SUM(r.miktar), 0)  AS toplam_miktar
    FROM ilac AS i
    LEFT JOIN recete AS r ON r.ilac_no = i.ilac_no
    GROUP BY i.ilac_no, i.ticari_ad
    ORDER BY recete_sayisi DESC, toplam_miktar DESC, i.ilac_no;
"""

S5_RECETESIZ_MUAYENELER = """
    SELECT
        m.muayene_id,
        m.muayene_tarihi,
        d.ad AS doktor_ad,
        h.ad AS hasta_ad
    FROM muayene AS m
    JOIN doktor  AS d ON d.doktor_no = m.doktor_no
    JOIN hasta   AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
    WHERE NOT EXISTS (
        SELECT 1
        FROM recete AS r
        WHERE r.doktor_no = m.doktor_no
          AND r.hasta_kimlik_no = m.hasta_kimlik_no
          AND r.recete_tarihi >= m.muayene_tarihi
    )
    ORDER BY m.muayene_tarihi DESC;
"""

S6_EKIM_EN_YUKSEK_MIKTAR = """
    SELECT
        r.recete_id,
        r.recete_tarihi,
        d.ad AS doktor_ad,
        h.ad AS hasta_ad,
        i.ticari_ad,
        r.miktar
    FROM recete AS r
    JOIN doktor AS d ON d.doktor_no = r.doktor_no
    JOIN hasta  AS h ON h.hasta_kimlik_no = r.hasta_kimlik_no
    JOIN ilac   AS i ON i.ilac_no = r.ilac_no
    WHERE r.recete_tarihi BETWEEN '2026-10-01' AND '2026-10-31'
    ORDER BY r.miktar DESC, r.recete_tarihi DESC
    LIMIT 5;
"""

# Sorgular sayfasinda sirayla gosterilir: (kod, tur, soru, sql)
IS_SORGULARI = [
    ("S1", "Çok tablolu JOIN",
     "Her reçetede hangi doktor, hangi hastaya, hangi ilaçtan ne kadar ve ne zaman yazmıştır?",
     S1_RECETE_DETAY),
    ("S2", "GROUP BY + HAVING",
     "En az 3 reçete yazmış doktorlar kimlerdir, kaç reçete ve toplam ne kadar ilaç "
     "yazmışlardır?",
     S2_COK_RECETE_YAZAN_DOKTORLAR),
    ("S3", "Alt sorgu",
     "Miktarı, tüm reçetelerin ortalama miktarından fazla olan reçeteler hangileridir?",
     S3_ORTALAMA_USTU_RECETELER),
    ("S4", "LEFT JOIN",
     "Tüm ilaçlar (hiç reçete edilmemiş olanlar dahil) kaç reçetede ve toplam ne kadar "
     "yazılmıştır?",
     S4_ILAC_RECETE_SAYILARI),
    ("S5", "NOT EXISTS",
     "Hangi muayenelerin ardından aynı doktor o hastaya hiç reçete yazmamıştır?",
     S5_RECETESIZ_MUAYENELER),
    ("S6", "Tarih aralığı + ORDER BY + LIMIT",
     "Ekim 2026'da yazılan reçetelerden miktarı en yüksek 5 tanesi hangileridir?",
     S6_EKIM_EN_YUKSEK_MIKTAR),
]
