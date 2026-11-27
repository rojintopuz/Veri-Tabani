from datetime import date

import psycopg
from flask import flash, redirect, render_template, request, url_for

from app.db import komut_calistir, tek_satir_getir, tum_satirlari_getir

from . import ilac_tedarik_bp
from . import sorgular as sql


def _db_hata_mesaji(hata):
    """Trigger veya fonksiyondan gelen RAISE EXCEPTION mesajini dondurur."""
    if hata.diag and hata.diag.message_primary:
        return hata.diag.message_primary
    return str(hata)


# --- ILAC CRUD ---

@ilac_tedarik_bp.get("/ilaclar")
def ilac_listele():
    ilaclar = tum_satirlari_getir(sql.ILAC_LISTELE)
    return render_template("ilac_tedarik/ilac_liste.html", ilaclar=ilaclar)


@ilac_tedarik_bp.get("/ilaclar/yeni")
def ilac_yeni_form():
    return render_template("ilac_tedarik/ilac_form.html", ilac=None)


@ilac_tedarik_bp.post("/ilaclar/yeni")
def ilac_ekle():
    ticari_ad = request.form["ticari_ad"].strip()
    if not ticari_ad:
        flash("İlacın ticari adı boş bırakılamaz.", "danger")
        return redirect(url_for("ilac_tedarik.ilac_yeni_form"))

    form_verisi = {
        "ticari_ad": ticari_ad,
        "formul": request.form.get("formul", "").strip() or None,
    }
    try:
        komut_calistir(sql.ILAC_EKLE, form_verisi)
        flash("İlaç eklendi.", "success")
    except psycopg.errors.UniqueViolation:
        flash("Bu ticari adla kayıtlı bir ilaç zaten var.", "danger")
    return redirect(url_for("ilac_tedarik.ilac_listele"))


@ilac_tedarik_bp.get("/ilaclar/<int:ilac_no>/duzenle")
def ilac_duzenle_form(ilac_no):
    ilac = tek_satir_getir(sql.ILAC_GETIR, {"ilac_no": ilac_no})
    if not ilac:
        flash("İlaç bulunamadı.", "warning")
        return redirect(url_for("ilac_tedarik.ilac_listele"))
    return render_template("ilac_tedarik/ilac_form.html", ilac=ilac)


@ilac_tedarik_bp.post("/ilaclar/<int:ilac_no>/duzenle")
def ilac_duzenle(ilac_no):
    ticari_ad = request.form["ticari_ad"].strip()
    if not ticari_ad:
        flash("İlacın ticari adı boş bırakılamaz.", "danger")
        return redirect(url_for("ilac_tedarik.ilac_duzenle_form", ilac_no=ilac_no))

    form_verisi = {
        "ilac_no": ilac_no,
        "ticari_ad": ticari_ad,
        "formul": request.form.get("formul", "").strip() or None,
    }
    try:
        komut_calistir(sql.ILAC_GUNCELLE, form_verisi)
        flash("İlaç güncellendi.", "success")
    except psycopg.errors.UniqueViolation:
        flash("Bu ticari adla kayıtlı başka bir ilaç var.", "danger")
    return redirect(url_for("ilac_tedarik.ilac_listele"))


@ilac_tedarik_bp.post("/ilaclar/<int:ilac_no>/sil")
def ilac_sil(ilac_no):
    try:
        komut_calistir(sql.ILAC_SIL, {"ilac_no": ilac_no})
        flash("İlaç silindi.", "success")
    except psycopg.errors.ForeignKeyViolation:
        flash(
            "Bu ilaca ait reçete, satış veya tedarik kaydı olduğu için silinemez.",
            "danger",
        )
    return redirect(url_for("ilac_tedarik.ilac_listele"))


# --- TEDARIKCI CRUD ---

@ilac_tedarik_bp.get("/tedarikciler")
def tedarikci_listele():
    tedarikciler = tum_satirlari_getir(sql.TEDARIKCI_LISTELE)
    return render_template("ilac_tedarik/tedarikci_liste.html", tedarikciler=tedarikciler)


@ilac_tedarik_bp.get("/tedarikciler/yeni")
def tedarikci_yeni_form():
    return render_template("ilac_tedarik/tedarikci_form.html", tedarikci=None)


@ilac_tedarik_bp.post("/tedarikciler/yeni")
def tedarikci_ekle():
    ad = request.form["ad"].strip()
    if not ad:
        flash("Tedarikçi adı boş bırakılamaz.", "danger")
        return redirect(url_for("ilac_tedarik.tedarikci_yeni_form"))

    form_verisi = {
        "ad": ad,
        "adres": request.form.get("adres", "").strip() or None,
    }
    komut_calistir(sql.TEDARIKCI_EKLE, form_verisi)
    flash("Tedarikçi eklendi.", "success")
    return redirect(url_for("ilac_tedarik.tedarikci_listele"))


@ilac_tedarik_bp.get("/tedarikciler/<int:tedarikci_no>/duzenle")
def tedarikci_duzenle_form(tedarikci_no):
    tedarikci = tek_satir_getir(sql.TEDARIKCI_GETIR, {"tedarikci_no": tedarikci_no})
    if not tedarikci:
        flash("Tedarikçi bulunamadı.", "warning")
        return redirect(url_for("ilac_tedarik.tedarikci_listele"))
    return render_template("ilac_tedarik/tedarikci_form.html", tedarikci=tedarikci)


@ilac_tedarik_bp.post("/tedarikciler/<int:tedarikci_no>/duzenle")
def tedarikci_duzenle(tedarikci_no):
    ad = request.form["ad"].strip()
    if not ad:
        flash("Tedarikçi adı boş bırakılamaz.", "danger")
        return redirect(
            url_for("ilac_tedarik.tedarikci_duzenle_form", tedarikci_no=tedarikci_no)
        )

    form_verisi = {
        "tedarikci_no": tedarikci_no,
        "ad": ad,
        "adres": request.form.get("adres", "").strip() or None,
    }
    komut_calistir(sql.TEDARIKCI_GUNCELLE, form_verisi)
    flash("Tedarikçi güncellendi.", "success")
    return redirect(url_for("ilac_tedarik.tedarikci_listele"))


@ilac_tedarik_bp.post("/tedarikciler/<int:tedarikci_no>/sil")
def tedarikci_sil(tedarikci_no):
    try:
        komut_calistir(sql.TEDARIKCI_SIL, {"tedarikci_no": tedarikci_no})
        flash("Tedarikçi silindi.", "success")
    except psycopg.errors.ForeignKeyViolation:
        flash("Bu tedarikçiye ait tedarik kaydı olduğu için silinemez.", "danger")
    return redirect(url_for("ilac_tedarik.tedarikci_listele"))


# --- TEDARIK CRUD ---

def _tedarik_form_secenekleri():
    return {
        "tedarikciler": tum_satirlari_getir(sql.TEDARIKCI_LISTELE),
        "eczaneler": tum_satirlari_getir(sql.ECZANE_SECENEKLERI),
        "ilaclar": tum_satirlari_getir(sql.ILAC_LISTELE),
    }


def _tedarik_formunu_oku():
    """Formdaki alanlari okur; eksik veya hatali alan varsa None dondurur."""
    try:
        return {
            "tedarikci_no": int(request.form["tedarikci_no"]),
            "eczane_no": int(request.form["eczane_no"]),
            "ilac_no": int(request.form["ilac_no"]),
            "miktar": int(request.form["miktar"]),
            "tedarik_tarihi": date.fromisoformat(request.form["tedarik_tarihi"]),
        }
    except (KeyError, ValueError):
        return None


def _tedarik_kayit_hatasi(hata):
    if isinstance(hata, psycopg.errors.UniqueViolation):
        return "Aynı tedarikçi, aynı gün, aynı eczaneye bu ilacı zaten getirmiş."
    if isinstance(hata, psycopg.errors.CheckViolation):
        return "Miktar 0'dan büyük olmalıdır."
    if isinstance(hata, psycopg.errors.ForeignKeyViolation):
        return "Seçilen tedarikçi, eczane veya ilaç bulunamadı."
    return _db_hata_mesaji(hata)


@ilac_tedarik_bp.get("/tedarikler")
def tedarik_listele():
    tedarikler = tum_satirlari_getir(sql.TEDARIK_LISTELE)
    return render_template("ilac_tedarik/tedarik_liste.html", tedarikler=tedarikler)


@ilac_tedarik_bp.get("/tedarikler/yeni")
def tedarik_yeni_form():
    return render_template(
        "ilac_tedarik/tedarik_form.html",
        tedarik=None,
        bugun=date.today().isoformat(),
        **_tedarik_form_secenekleri(),
    )


@ilac_tedarik_bp.post("/tedarikler/yeni")
def tedarik_ekle():
    form_verisi = _tedarik_formunu_oku()
    if form_verisi is None:
        flash("Lütfen tüm alanları doğru doldurun.", "danger")
        return redirect(url_for("ilac_tedarik.tedarik_yeni_form"))
    try:
        komut_calistir(sql.TEDARIK_EKLE, form_verisi)
        flash("Tedarik eklendi (denetim kaydı otomatik oluşturuldu).", "success")
    except psycopg.Error as hata:
        flash(_tedarik_kayit_hatasi(hata), "danger")
        return redirect(url_for("ilac_tedarik.tedarik_yeni_form"))
    return redirect(url_for("ilac_tedarik.tedarik_listele"))


@ilac_tedarik_bp.get("/tedarikler/<int:tedarik_id>/duzenle")
def tedarik_duzenle_form(tedarik_id):
    tedarik = tek_satir_getir(sql.TEDARIK_GETIR, {"tedarik_id": tedarik_id})
    if not tedarik:
        flash("Tedarik kaydı bulunamadı.", "warning")
        return redirect(url_for("ilac_tedarik.tedarik_listele"))
    return render_template(
        "ilac_tedarik/tedarik_form.html",
        tedarik=tedarik,
        bugun=date.today().isoformat(),
        **_tedarik_form_secenekleri(),
    )


@ilac_tedarik_bp.post("/tedarikler/<int:tedarik_id>/duzenle")
def tedarik_duzenle(tedarik_id):
    form_verisi = _tedarik_formunu_oku()
    if form_verisi is None:
        flash("Lütfen tüm alanları doğru doldurun.", "danger")
        return redirect(url_for("ilac_tedarik.tedarik_duzenle_form", tedarik_id=tedarik_id))
    form_verisi["tedarik_id"] = tedarik_id
    try:
        komut_calistir(sql.TEDARIK_GUNCELLE, form_verisi)
        flash("Tedarik güncellendi (denetim kaydı otomatik oluşturuldu).", "success")
    except psycopg.Error as hata:
        flash(_tedarik_kayit_hatasi(hata), "danger")
        return redirect(url_for("ilac_tedarik.tedarik_duzenle_form", tedarik_id=tedarik_id))
    return redirect(url_for("ilac_tedarik.tedarik_listele"))


@ilac_tedarik_bp.post("/tedarikler/<int:tedarik_id>/sil")
def tedarik_sil(tedarik_id):
    komut_calistir(sql.TEDARIK_SIL, {"tedarik_id": tedarik_id})
    flash("Tedarik silindi (denetim kaydı otomatik oluşturuldu).", "success")
    return redirect(url_for("ilac_tedarik.tedarik_listele"))


# --- RAPOR (view + fonksiyon + trigger) ---

@ilac_tedarik_bp.get("/rapor")
def rapor():
    ozet = tum_satirlari_getir(sql.ILAC_TEDARIK_OZETI)
    denetim_kayitlari = tum_satirlari_getir(sql.TEDARIK_DENETIM_SON_KAYITLAR)
    eczaneler = tum_satirlari_getir(sql.ECZANE_SECENEKLERI)
    ilaclar = tum_satirlari_getir(sql.ILAC_LISTELE)

    stok = None
    secim = {
        "eczane_no": request.args.get("eczane_no", type=int),
        "ilac_no": request.args.get("ilac_no", type=int),
    }
    if secim["eczane_no"] is not None and secim["ilac_no"] is not None:
        try:
            stok = tek_satir_getir(sql.ECZANE_ILAC_STOK, secim)["stok"]
        except psycopg.errors.RaiseException as hata:
            flash(_db_hata_mesaji(hata), "danger")

    return render_template(
        "ilac_tedarik/rapor.html",
        ozet=ozet,
        denetim_kayitlari=denetim_kayitlari,
        eczaneler=eczaneler,
        ilaclar=ilaclar,
        secim=secim,
        stok=stok,
    )


# --- SORGULAR ---

@ilac_tedarik_bp.get("/sorgular")
def sorgular():
    sonuclar = []
    for sorgu in sql.SORGU_LISTESI:
        satirlar = tum_satirlari_getir(sorgu["sql"])
        sonuclar.append({**sorgu, "satirlar": satirlar})
    return render_template("ilac_tedarik/sorgular.html", sonuclar=sonuclar)
