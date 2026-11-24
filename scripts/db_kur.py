"""db/ klasorundeki SQL dosyalarini sirayla calistirip veritabanini sifirdan kurar.
Kullanim: python scripts/db_kur.py
Ayrica teslim icin tek dosya uretir: db/build/tam_kurulum.sql
"""
import os
import sys
from pathlib import Path
import psycopg
from dotenv import load_dotenv

KOK_DIZIN = Path(__file__).resolve().parent.parent
DB_DIZINI = KOK_DIZIN / "db"
CIKTI_DOSYASI = DB_DIZINI / "build" / "tam_kurulum.sql"

KURULUM_KLASORLERI = [
    "00_sema",
    "10_varliklar",
    "20_iliskiler",
    "30_gorunumler",
    "40_fonksiyonlar",
    "50_tetikleyiciler",
    "60_veriler",
]


def sql_dosyalarini_bul():
    dosyalar = []
    for klasor_adi in KURULUM_KLASORLERI:
        klasor = DB_DIZINI / klasor_adi
        if klasor.exists():
            dosyalar.extend(sorted(klasor.glob("*.sql")))
    return dosyalar


def main():
    load_dotenv(KOK_DIZIN / ".env")
    veritabani_url = os.environ.get("DATABASE_URL")
    if not veritabani_url:
        sys.exit("HATA: DATABASE_URL tanimli degil (.env veya Codespaces secret).")

    dosyalar = sql_dosyalarini_bul()
    birlesik_sql = ["SET search_path TO eczane, public;\n"]

    with psycopg.connect(veritabani_url, autocommit=False) as baglanti:
        for dosya in dosyalar:
            goreli_yol = dosya.relative_to(KOK_DIZIN)
            sql_metni = dosya.read_text(encoding="utf-8")
            try:
                baglanti.execute("SET search_path TO eczane, public")
                baglanti.execute(sql_metni)
            except psycopg.Error as hata:
                baglanti.rollback()
                sys.exit(f"HATA -> {goreli_yol}\n{hata}")
            birlesik_sql.append(f"\n-- >>> {goreli_yol}\n{sql_metni}")
            print(f"OK  {goreli_yol}")
        baglanti.commit()

    CIKTI_DOSYASI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI_DOSYASI.write_text("".join(birlesik_sql), encoding="utf-8")
    print(f"\nKurulum tamam. Tek dosya: {CIKTI_DOSYASI.relative_to(KOK_DIZIN)}")


if __name__ == "__main__":
    main()