from datetime import date

import psycopg
from flask import flash, redirect, render_template, request, url_for

from app.db import komut_calistir, tek_satir_getir, tum_satirlari_getir

from . import doktor_recete_bp
from . import sorgular as sql


# --- Yardimcilar ---

def _doktor_formunu_oku():
    """Formdaki doktor alanlarini okur. Hatali alan varsa (veri, hata) dondurur."""
    form_verisi = {
        "ad": request.form.get("ad", "").strip(),
        "uzmanlik_alani": request.form.get("uzmanlik_alani", "").strip(),
        "deneyim_yili": request.form.get("deneyim_yili", "").strip(),
    }
    if not form_verisi["ad"] or not form_verisi["uzmanlik_alani"]:
        return form_verisi, "Doktor adı ve uzmanlık alanı boş bırakılamaz."
    try:
        form_verisi["deneyim_yili"] = int(form_verisi["deneyim_yili"])
    except ValueError:
        return form_verisi, "Deneyim yılı tam sayı olmalıdır."
    if not 0 <= form_verisi["deneyim_yili"] <= 65:
        return form_verisi, "Deneyim yılı 0 ile 65 arasında olmalıdır."
    return form_verisi, None


def _recete_formunu_oku():
    """Formdaki recete alanlarini okur. Hatali alan varsa (veri, hata) dondurur."""
    form_verisi = {
        "doktor_no": request.form.get("doktor_no", "").strip(),
        "hasta_kimlik_no": request.form.get("hasta_kimlik_no", "").strip(),
        "ilac_no": request.form.get("ilac_no", "").strip(),
        "recete_tarihi": request.form.get("recete_tarihi", "").strip(),
        "miktar": request.form.get("miktar", "").strip(),
    }
    if not all(form_verisi.values()):
        return form_verisi, "Tüm alanlar doldurulmalıdır."
    try:
        form_verisi["doktor_no"] = int(form_verisi["doktor_no"])
        form_verisi["ilac_no"] = int(form_verisi["ilac_no"])
        form_verisi["miktar"] = int(form_verisi["miktar"])
        form_verisi["recete_tarihi"] = date.fromisoformat(form_verisi["recete_tarihi"])
    except ValueError:
        return form_verisi, "Doktor, ilaç ve miktar sayı olmalı; tarih geçerli olmalıdır."
    if form_verisi["miktar"] <= 0:
        return form_verisi, "Miktar 0'dan büyük olmalıdır."
    return form_verisi, None


def _recete_hata_mesaji(hata):
    """Recete INSERT/UPDATE sirasinda gelen DB hatasini Turkce mesaja cevirir."""
    if isinstance(hata, psycopg.errors.RaiseException):
        # Trigger: muayene sarti veya gelecek tarih
        return "Reçete kaydedilemedi: " + hata.diag.message_primary
    if isinstance(hata, psycopg.errors.UniqueViolation):
        return "Bu doktor aynı gün bu hastaya bu ilacı zaten reçete etmiş."
    if isinstance(hata, psycopg.errors.ForeignKeyViolation):
        return "Seçilen doktor, hasta veya ilaç bulunamadı."
    if isinstance(hata, psycopg.errors.CheckViolation):
        return "Miktar 0'dan büyük olmalıdır."
    return "Reçete kaydedilemedi, girilen bilgileri kontrol edin."


def _recete_formunu_goster(recete, duzenleme):
    return render_template(
        "doktor_recete/recete_form.html",
        recete=recete,
        duzenleme=duzenleme,
        doktorlar=tum_satirlari_getir(sql.DOKTOR_SECENEKLERI),
        hastalar=tum_satirlari_getir(sql.HASTA_SECENEKLERI),
        ilaclar=tum_satirlari_getir(sql.ILAC_SECENEKLERI),
        bugun=date.today().isoformat(),
    )


RECETE_DB_HATALARI = (
    psycopg.errors.RaiseException,
    psycopg.errors.UniqueViolation,
    psycopg.errors.ForeignKeyViolation,
    psycopg.errors.CheckViolation,
)


# --- DOKTOR CRUD ---

@doktor_recete_bp.get("/doktorlar")
def doktor_listele():
    doktorlar = tum_satirlari_getir(sql.DOKTOR_LISTELE)
    return render_template("doktor_recete/doktor_liste.html", doktorlar=doktorlar)


@doktor_recete_bp.route("/doktorlar/yeni", methods=["GET", "POST"])
def doktor_ekle():
    if request.method == "GET":
        return render_template("doktor_recete/doktor_form.html", doktor=None)

    form_verisi, hata = _doktor_formunu_oku()
    if hata:
        flash(hata, "danger")
        return render_template("doktor_recete/doktor_form.html", doktor=form_verisi)
    try:
        komut_calistir(sql.DOKTOR_EKLE, form_verisi)
    except psycopg.errors.CheckViolation:
        flash("Deneyim yılı 0 ile 65 arasında olmalıdır.", "danger")
        return render_template("doktor_recete/doktor_form.html", doktor=form_verisi)
    flash("Doktor eklendi.", "success")
    return redirect(url_for("doktor_recete.doktor_listele"))


@doktor_recete_bp.route("/doktorlar/<int:doktor_no>/duzenle", methods=["GET", "POST"])
def doktor_duzenle(doktor_no):
    if request.method == "GET":
        doktor = tek_satir_getir(sql.DOKTOR_GETIR, {"doktor_no": doktor_no})
        if not doktor:
            flash("Doktor bulunamadı.", "warning")
            return redirect(url_for("doktor_recete.doktor_listele"))
        return render_template("doktor_recete/doktor_form.html", doktor=doktor)

    form_verisi, hata = _doktor_formunu_oku()
    form_verisi["doktor_no"] = doktor_no
    if hata:
        flash(hata, "danger")
        return render_template("doktor_recete/doktor_form.html", doktor=form_verisi)
    try:
        guncellenen = komut_calistir(sql.DOKTOR_GUNCELLE, form_verisi)
    except psycopg.errors.CheckViolation:
        flash("Deneyim yılı 0 ile 65 arasında olmalıdır.", "danger")
        return render_template("doktor_recete/doktor_form.html", doktor=form_verisi)
    if guncellenen:
        flash("Doktor güncellendi.", "success")
    else:
        flash("Doktor bulunamadı.", "warning")
    return redirect(url_for("doktor_recete.doktor_listele"))


@doktor_recete_bp.post("/doktorlar/<int:doktor_no>/sil")
def doktor_sil(doktor_no):
    try:
        silinen = komut_calistir(sql.DOKTOR_SIL, {"doktor_no": doktor_no})
    except psycopg.errors.ForeignKeyViolation:
        flash("Bu doktorun muayene veya reçete kaydı olduğu için silinemez.", "danger")
        return redirect(url_for("doktor_recete.doktor_listele"))
    if silinen:
        flash("Doktor silindi.", "success")
    else:
        flash("Doktor bulunamadı.", "warning")
    return redirect(url_for("doktor_recete.doktor_listele"))


# --- RECETE CRUD ---

@doktor_recete_bp.get("/receteler")
def recete_listele():
    receteler = tum_satirlari_getir(sql.RECETE_LISTELE)
    return render_template("doktor_recete/recete_liste.html", receteler=receteler)


@doktor_recete_bp.route("/receteler/yeni", methods=["GET", "POST"])
def recete_ekle():
    if request.method == "GET":
        return _recete_formunu_goster(None, duzenleme=False)

    form_verisi, hata = _recete_formunu_oku()
    if not hata:
        try:
            komut_calistir(sql.RECETE_EKLE, form_verisi)
        except RECETE_DB_HATALARI as db_hatasi:
            hata = _recete_hata_mesaji(db_hatasi)
    if hata:
        flash(hata, "danger")
        return _recete_formunu_goster(form_verisi, duzenleme=False)
    flash("Reçete eklendi.", "success")
    return redirect(url_for("doktor_recete.recete_listele"))


@doktor_recete_bp.route("/receteler/<int:recete_id>/duzenle", methods=["GET", "POST"])
def recete_duzenle(recete_id):
    if request.method == "GET":
        recete = tek_satir_getir(sql.RECETE_GETIR, {"recete_id": recete_id})
        if not recete:
            flash("Reçete bulunamadı.", "warning")
            return redirect(url_for("doktor_recete.recete_listele"))
        return _recete_formunu_goster(recete, duzenleme=True)

    form_verisi, hata = _recete_formunu_oku()
    form_verisi["recete_id"] = recete_id
    guncellenen = 0
    if not hata:
        try:
            guncellenen = komut_calistir(sql.RECETE_GUNCELLE, form_verisi)
        except RECETE_DB_HATALARI as db_hatasi:
            hata = _recete_hata_mesaji(db_hatasi)
    if hata:
        flash(hata, "danger")
        return _recete_formunu_goster(form_verisi, duzenleme=True)
    if guncellenen:
        flash("Reçete güncellendi.", "success")
    else:
        flash("Reçete bulunamadı.", "warning")
    return redirect(url_for("doktor_recete.recete_listele"))


@doktor_recete_bp.post("/receteler/<int:recete_id>/sil")
def recete_sil(recete_id):
    try:
        silinen = komut_calistir(sql.RECETE_SIL, {"recete_id": recete_id})
    except psycopg.errors.ForeignKeyViolation:
        flash("Bu reçeteye bağlı kayıt olduğu için silinemez.", "danger")
        return redirect(url_for("doktor_recete.recete_listele"))
    if silinen:
        flash("Reçete silindi.", "success")
    else:
        flash("Reçete bulunamadı.", "warning")
    return redirect(url_for("doktor_recete.recete_listele"))


# --- RAPOR ve SORGULAR ---

@doktor_recete_bp.get("/rapor")
def rapor():
    istatistikler = tum_satirlari_getir(sql.DOKTOR_RECETE_ISTATISTIGI)
    doktorlar = tum_satirlari_getir(sql.DOKTOR_SECENEKLERI)

    secilen_doktor_no = request.args.get("doktor_no", type=int)
    en_cok_ilac = None
    if secilen_doktor_no is not None:
        try:
            en_cok_ilac = tek_satir_getir(
                sql.DOKTOR_EN_COK_YAZDIGI_ILAC, {"doktor_no": secilen_doktor_no}
            )
        except psycopg.errors.RaiseException:
            flash("Seçilen doktor bulunamadı.", "warning")
            secilen_doktor_no = None

    return render_template(
        "doktor_recete/rapor.html",
        istatistikler=istatistikler,
        doktorlar=doktorlar,
        secilen_doktor_no=secilen_doktor_no,
        en_cok_ilac=en_cok_ilac,
    )


@doktor_recete_bp.get("/sorgular")
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
    return render_template("doktor_recete/sorgular.html", sonuclar=sonuclar)
