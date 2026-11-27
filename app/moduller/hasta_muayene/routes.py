import re
from datetime import date

import psycopg
from flask import flash, redirect, render_template, request, url_for

from app.db import komut_calistir, tek_satir_getir, tum_satirlari_getir

from . import hasta_muayene_bp
from . import sorgular as sql

KIMLIK_NO_DESENI = re.compile(r"^[1-9][0-9]{10}$")


# --- Yardimcilar ---

def _hasta_formunu_oku(kimlik_no=None):
    """Formdaki hasta alanlarini okur. Hatali alan varsa (veri, hata) dondurur.

    Duzenlemede kimlik no (PK) degistirilmez; URL'deki deger kullanilir.
    """
    form_verisi = {
        "hasta_kimlik_no": kimlik_no or request.form.get("hasta_kimlik_no", "").strip(),
        "ad": request.form.get("ad", "").strip(),
        "adres": request.form.get("adres", "").strip() or None,
        "yas": request.form.get("yas", "").strip(),
    }
    if not KIMLIK_NO_DESENI.match(form_verisi["hasta_kimlik_no"]):
        return form_verisi, "Kimlik no 11 haneli olmalı ve 0 ile başlamamalıdır."
    if not form_verisi["ad"]:
        return form_verisi, "Hasta adı boş bırakılamaz."
    try:
        form_verisi["yas"] = int(form_verisi["yas"])
    except ValueError:
        return form_verisi, "Yaş tam sayı olmalıdır."
    if not 0 <= form_verisi["yas"] <= 130:
        return form_verisi, "Yaş 0 ile 130 arasında olmalıdır."
    return form_verisi, None


def _muayene_formunu_oku():
    """Formdaki muayene alanlarini okur. Hatali alan varsa (veri, hata) dondurur."""
    form_verisi = {
        "doktor_no": request.form.get("doktor_no", "").strip(),
        "hasta_kimlik_no": request.form.get("hasta_kimlik_no", "").strip(),
        "muayene_tarihi": request.form.get("muayene_tarihi", "").strip(),
    }
    if not all(form_verisi.values()):
        return form_verisi, "Tüm alanlar doldurulmalıdır."
    try:
        form_verisi["doktor_no"] = int(form_verisi["doktor_no"])
        form_verisi["muayene_tarihi"] = date.fromisoformat(form_verisi["muayene_tarihi"])
    except ValueError:
        return form_verisi, "Doktor seçimi veya tarih geçersiz."
    return form_verisi, None


def _muayene_hata_mesaji(hata):
    """Muayene INSERT/UPDATE sirasinda gelen DB hatasini Turkce mesaja cevirir."""
    if isinstance(hata, psycopg.errors.RaiseException):
        # trg_muayene_tarih_kontrol
        return "Muayene tarihi gelecekte olamaz. Bugünün veya geçmiş bir günün tarihini girin."
    if isinstance(hata, psycopg.errors.UniqueViolation):
        return "Bu doktor bu hastayı aynı gün zaten muayene etmiş."
    if isinstance(hata, psycopg.errors.ForeignKeyViolation):
        return "Seçilen doktor veya hasta bulunamadı."
    return "Muayene kaydedilemedi, girilen bilgileri kontrol edin."


def _muayene_formunu_goster(muayene, duzenleme):
    return render_template(
        "hasta_muayene/muayene_form.html",
        muayene=muayene,
        duzenleme=duzenleme,
        doktorlar=tum_satirlari_getir(sql.DOKTOR_SECENEKLERI),
        hastalar=tum_satirlari_getir(sql.HASTA_SECENEKLERI),
        bugun=date.today().isoformat(),
    )


MUAYENE_DB_HATALARI = (
    psycopg.errors.RaiseException,
    psycopg.errors.UniqueViolation,
    psycopg.errors.ForeignKeyViolation,
)


# --- HASTA CRUD ---

@hasta_muayene_bp.get("/hastalar")
def hasta_listele():
    hastalar = tum_satirlari_getir(sql.HASTA_LISTELE)
    return render_template("hasta_muayene/hasta_liste.html", hastalar=hastalar)


@hasta_muayene_bp.route("/hastalar/yeni", methods=["GET", "POST"])
def hasta_ekle():
    if request.method == "GET":
        return render_template("hasta_muayene/hasta_form.html", hasta=None, duzenleme=False)

    form_verisi, hata = _hasta_formunu_oku()
    if not hata:
        try:
            komut_calistir(sql.HASTA_EKLE, form_verisi)
        except psycopg.errors.UniqueViolation:
            hata = "Bu kimlik numarasıyla kayıtlı bir hasta zaten var."
        except psycopg.errors.CheckViolation:
            hata = "Kimlik no, ad veya yaş kurallara uymuyor."
    if hata:
        flash(hata, "danger")
        return render_template("hasta_muayene/hasta_form.html", hasta=form_verisi, duzenleme=False)
    flash("Hasta eklendi.", "success")
    return redirect(url_for("hasta_muayene.hasta_listele"))


@hasta_muayene_bp.route("/hastalar/<hasta_kimlik_no>/duzenle", methods=["GET", "POST"])
def hasta_duzenle(hasta_kimlik_no):
    if request.method == "GET":
        hasta = tek_satir_getir(sql.HASTA_GETIR, {"hasta_kimlik_no": hasta_kimlik_no})
        if not hasta:
            flash("Hasta bulunamadı.", "warning")
            return redirect(url_for("hasta_muayene.hasta_listele"))
        return render_template("hasta_muayene/hasta_form.html", hasta=hasta, duzenleme=True)

    form_verisi, hata = _hasta_formunu_oku(kimlik_no=hasta_kimlik_no)
    guncellenen = 0
    if not hata:
        try:
            guncellenen = komut_calistir(sql.HASTA_GUNCELLE, form_verisi)
        except psycopg.errors.CheckViolation:
            hata = "Ad veya yaş kurallara uymuyor."
    if hata:
        flash(hata, "danger")
        return render_template("hasta_muayene/hasta_form.html", hasta=form_verisi, duzenleme=True)
    if guncellenen:
        flash("Hasta güncellendi.", "success")
    else:
        flash("Hasta bulunamadı.", "warning")
    return redirect(url_for("hasta_muayene.hasta_listele"))


@hasta_muayene_bp.post("/hastalar/<hasta_kimlik_no>/sil")
def hasta_sil(hasta_kimlik_no):
    try:
        silinen = komut_calistir(sql.HASTA_SIL, {"hasta_kimlik_no": hasta_kimlik_no})
    except psycopg.errors.ForeignKeyViolation:
        flash("Bu hastanın muayene, reçete veya satış kaydı olduğu için silinemez.", "danger")
        return redirect(url_for("hasta_muayene.hasta_listele"))
    if silinen:
        flash("Hasta silindi.", "success")
    else:
        flash("Hasta bulunamadı.", "warning")
    return redirect(url_for("hasta_muayene.hasta_listele"))


# --- MUAYENE CRUD ---

@hasta_muayene_bp.get("/muayeneler")
def muayene_listele():
    muayeneler = tum_satirlari_getir(sql.MUAYENE_LISTELE)
    return render_template("hasta_muayene/muayene_liste.html", muayeneler=muayeneler)


@hasta_muayene_bp.route("/muayeneler/yeni", methods=["GET", "POST"])
def muayene_ekle():
    if request.method == "GET":
        return _muayene_formunu_goster(None, duzenleme=False)

    form_verisi, hata = _muayene_formunu_oku()
    if not hata:
        try:
            komut_calistir(sql.MUAYENE_EKLE, form_verisi)
        except MUAYENE_DB_HATALARI as db_hatasi:
            hata = _muayene_hata_mesaji(db_hatasi)
    if hata:
        flash(hata, "danger")
        return _muayene_formunu_goster(form_verisi, duzenleme=False)
    flash("Muayene eklendi.", "success")
    return redirect(url_for("hasta_muayene.muayene_listele"))


@hasta_muayene_bp.route("/muayeneler/<int:muayene_id>/duzenle", methods=["GET", "POST"])
def muayene_duzenle(muayene_id):
    if request.method == "GET":
        muayene = tek_satir_getir(sql.MUAYENE_GETIR, {"muayene_id": muayene_id})
        if not muayene:
            flash("Muayene bulunamadı.", "warning")
            return redirect(url_for("hasta_muayene.muayene_listele"))
        return _muayene_formunu_goster(muayene, duzenleme=True)

    form_verisi, hata = _muayene_formunu_oku()
    form_verisi["muayene_id"] = muayene_id
    guncellenen = 0
    if not hata:
        try:
            guncellenen = komut_calistir(sql.MUAYENE_GUNCELLE, form_verisi)
        except MUAYENE_DB_HATALARI as db_hatasi:
            hata = _muayene_hata_mesaji(db_hatasi)
    if hata:
        flash(hata, "danger")
        return _muayene_formunu_goster(form_verisi, duzenleme=True)
    if guncellenen:
        flash("Muayene güncellendi.", "success")
    else:
        flash("Muayene bulunamadı.", "warning")
    return redirect(url_for("hasta_muayene.muayene_listele"))


@hasta_muayene_bp.post("/muayeneler/<int:muayene_id>/sil")
def muayene_sil(muayene_id):
    silinen = komut_calistir(sql.MUAYENE_SIL, {"muayene_id": muayene_id})
    if silinen:
        flash("Muayene silindi.", "success")
    else:
        flash("Muayene bulunamadı.", "warning")
    return redirect(url_for("hasta_muayene.muayene_listele"))


# --- RAPOR ve SORGULAR ---

@hasta_muayene_bp.get("/rapor")
def rapor():
    ozetler = tum_satirlari_getir(sql.HASTA_MUAYENE_OZETI)
    hastalar = tum_satirlari_getir(sql.HASTA_SECENEKLERI)

    secilen_kimlik_no = request.args.get("hasta_kimlik_no", "").strip() or None
    gecmis = None
    if secilen_kimlik_no:
        try:
            gecmis = tum_satirlari_getir(
                sql.HASTA_MUAYENE_GECMISI, {"hasta_kimlik_no": secilen_kimlik_no}
            )
        except psycopg.errors.RaiseException:
            # fn_hasta_muayene_gecmisi: hasta yoksa hata verir
            flash("Seçilen hasta bulunamadı.", "warning")
            secilen_kimlik_no = None

    return render_template(
        "hasta_muayene/rapor.html",
        ozetler=ozetler,
        hastalar=hastalar,
        secilen_kimlik_no=secilen_kimlik_no,
        gecmis=gecmis,
    )


@hasta_muayene_bp.get("/sorgular")
def sorgular():
    sonuclar = []
    for kod, tur, soru, sorgu in sql.IS_SORGULARI:
        sonuclar.append({
            "kod": kod,
            "tur": tur,
            "soru": soru,
            "sql": sorgu.strip(),
            "satirlar": tum_satirlari_getir(sorgu),
        })
    return render_template("hasta_muayene/sorgular.html", sonuclar=sonuclar)
