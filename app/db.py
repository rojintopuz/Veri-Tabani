"""Ortak veritabani erisim katmani. SADECE bu modul baglanti acar."""
import os
from contextlib import contextmanager
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
VERITABANI_SEMASI = "eczane"


@contextmanager
def baglanti_ac():
    """Blok hatasiz biterse COMMIT, hata olursa ROLLBACK yapar."""
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as baglanti:
        baglanti.execute(f"SET search_path TO {VERITABANI_SEMASI}, public")
        yield baglanti


def tum_satirlari_getir(sql, parametreler=None):
    with baglanti_ac() as baglanti:
        return baglanti.execute(sql, parametreler).fetchall()


def tek_satir_getir(sql, parametreler=None):
    with baglanti_ac() as baglanti:
        return baglanti.execute(sql, parametreler).fetchone()


def komut_calistir(sql, parametreler=None):
    """INSERT / UPDATE / DELETE icin. Etkilenen satir sayisini dondurur."""
    with baglanti_ac() as baglanti:
        return baglanti.execute(sql, parametreler).rowcount