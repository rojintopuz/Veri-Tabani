import psycopg
from flask import flash, redirect, render_template, request, url_for
from app.db import komut_calistir, tek_satir_getir, tum_satirlari_getir
from . import eczane_satis_bp
from . import sorgular as sql


# --- ECZANE CRUD ---

@eczane_satis_bp.get("/eczaneler")
def eczane_listele():
    eczaneler = tum_satirlari_getir(sql.ECZANE_LISTELE)
    return render_template("eczane_satis/eczane_liste.html", eczaneler=eczaneler)


@eczane_satis_bp.get("/eczaneler/yeni")
def eczane_yeni_form():
    return render_template("eczane_satis/eczane_form.html", eczane=None)


@eczane_satis_bp.post("/eczaneler/yeni")
def eczane_ekle():
    form_verisi = {
        "ad": request.form["ad"].strip(),
        "adres": request.form.get("adres", "").strip() or None,
    }
    try:
        komut_calistir(sql.ECZANE_EKLE, form_verisi)
        flash("Eczane eklendi.", "success")
    except psycopg.errors.CheckViolation:
        flash("Eczane bilgileri kısıt kurallarına uymuyor.", "danger")
    return redirect(url_for("eczane_satis.eczane_listele"))


@eczane_satis_bp.get("/eczaneler/<int:eczane_no>/duzenle")
def eczane_duzenle_form(eczane_no):
    eczane = tek_satir_getir(sql.ECZANE_GETIR, {"eczane_no": eczane_no})
    if not eczane:
        flash("Eczane bulunamadı.", "warning")
        return redirect(url_for("eczane_satis.eczane_listele"))
    return render_template("eczane_satis/eczane_form.html", eczane=eczane)


@eczane_satis_bp.post("/eczaneler/<int:eczane_no>/duzenle")
def eczane_duzenle(eczane_no):
    form_verisi = {
        "eczane_no": eczane_no,
        "ad": request.form["ad"].strip(),
        "adres": request.form.get("adres", "").strip() or None,
    }
    try:
        komut_calistir(sql.ECZANE_GUNCELLE, form_verisi)
        flash("Eczane güncellendi.", "success")
    except psycopg.errors.CheckViolation:
        flash("Eczane bilgileri kısıt kurallarına uymuyor.", "danger")
    return redirect(url_for("eczane_satis.eczane_listele"))


@eczane_satis_bp.post("/eczaneler/<int:eczane_no>/sil")
def eczane_sil(eczane_no):
    try:
        komut_calistir(sql.ECZANE_SIL, {"eczane_no": eczane_no})
        flash("Eczane silindi.", "success")
    except psycopg.errors.ForeignKeyViolation:
        flash("Bu eczaneye ait satış veya tedarik kaydı olduğu için silinemez.", "danger")
    return redirect(url_for("eczane_satis.eczane_listele"))


# --- ECZANE TELEFON CRUD ---

@eczane_satis_bp.get("/telefonlar")
def telefon_listele():
    telefonlar = tum_satirlari_getir(sql.TELEFON_LISTELE)
    return render_template("eczane_satis/telefon_liste.html", telefonlar=telefonlar)


@eczane_satis_bp.get("/telefonlar/yeni")
def telefon_yeni_form():
    eczaneler = tum_satirlari_getir(sql.ECZANE_LISTELE)
    return render_template(
        "eczane_satis/telefon_form.html", telefon=None, eczaneler=eczaneler
    )


@eczane_satis_bp.post("/telefonlar/yeni")
def telefon_ekle():
    form_verisi = {
        "eczane_no": int(request.form["eczane_no"]),
        "telefon_no": request.form["telefon_no"].strip(),
    }
    try:
        komut_calistir(sql.TELEFON_EKLE, form_verisi)
        flash("Telefon numarası eklendi.", "success")
    except psycopg.errors.UniqueViolation:
        flash("Bu eczane için bu telefon numarası zaten kayıtlı.", "danger")
    except psycopg.errors.CheckViolation:
        flash("Telefon numarası 0 ile başlayan 11 haneli rakam olmalıdır (örn: 02241234567).", "danger")
    except psycopg.errors.ForeignKeyViolation:
        flash("Seçilen eczane bulunamadı.", "danger")
    return redirect(url_for("eczane_satis.telefon_listele"))


@eczane_satis_bp.get("/telefonlar/<int:eczane_no>/<telefon_no>/duzenle")
def telefon_duzenle_form(eczane_no, telefon_no):
    telefon = tek_satir_getir(
        sql.TELEFON_GETIR, {"eczane_no": eczane_no, "telefon_no": telefon_no}
    )
    if not telefon:
        flash("Telefon kaydı bulunamadı.", "warning")
        return redirect(url_for("eczane_satis.telefon_listele"))
    eczaneler = tum_satirlari_getir(sql.ECZANE_LISTELE)
    return render_template(
        "eczane_satis/telefon_form.html", telefon=telefon, eczaneler=eczaneler
    )


@eczane_satis_bp.post("/telefonlar/<int:eczane_no>/<telefon_no>/duzenle")
def telefon_duzenle(eczane_no, telefon_no):
    form_verisi = {
        "eski_eczane_no": eczane_no,
        "eski_telefon_no": telefon_no,
        "yeni_eczane_no": int(request.form["eczane_no"]),
        "yeni_telefon_no": request.form["telefon_no"].strip(),
    }
    try:
        komut_calistir(sql.TELEFON_GUNCELLE, form_verisi)
        flash("Telefon numarası güncellendi.", "success")
    except psycopg.errors.UniqueViolation:
        flash("Bu eczane için bu telefon numarası zaten kayıtlı.", "danger")
    except psycopg.errors.CheckViolation:
        flash("Telefon numarası 0 ile başlayan 11 haneli rakam olmalıdır.", "danger")
    return redirect(url_for("eczane_satis.telefon_listele"))


@eczane_satis_bp.post("/telefonlar/<int:eczane_no>/<telefon_no>/sil")
def telefon_sil(eczane_no, telefon_no):
    komut_calistir(
        sql.TELEFON_SIL, {"eczane_no": eczane_no, "telefon_no": telefon_no}
    )
    flash("Telefon numarası silindi.", "success")
    return redirect(url_for("eczane_satis.telefon_listele"))