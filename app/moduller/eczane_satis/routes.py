from datetime import date
from decimal import Decimal, InvalidOperation
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
    ad = request.form["ad"].strip()
    if not ad:
        flash("Eczane adı boş bırakılamaz.", "danger")
        return redirect(url_for("eczane_satis.eczane_listele"))

    form_verisi = {
        "ad": ad,
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
    ad = request.form["ad"].strip()
    if not ad:
        flash("Eczane adı boş bırakılamaz.", "danger")
        return redirect(url_for("eczane_satis.eczane_listele"))

    form_verisi = {
        "eczane_no": eczane_no,
        "ad": ad,
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
    except psycopg.errors.ForeignKeyViolation:
        flash("Seçilen eczane bulunamadı.", "danger")
    return redirect(url_for("eczane_satis.telefon_listele"))


@eczane_satis_bp.post("/telefonlar/<int:eczane_no>/<telefon_no>/sil")
def telefon_sil(eczane_no, telefon_no):
    komut_calistir(
        sql.TELEFON_SIL, {"eczane_no": eczane_no, "telefon_no": telefon_no}
    )
    flash("Telefon numarası silindi.", "success")
    return redirect(url_for("eczane_satis.telefon_listele"))


# --- SATIS CRUD ---

def _satis_formunu_oku():
    """Formdaki satis alanlarini okur ve dogrular. (veri, hata) dondurur."""
    form_verisi = {
        "eczane_no": request.form.get("eczane_no", "").strip(),
        "hasta_kimlik_no": request.form.get("hasta_kimlik_no", "").strip(),
        "ilac_no": request.form.get("ilac_no", "").strip(),
        "fiyat": request.form.get("fiyat", "").strip(),
        "satis_tarihi": request.form.get("satis_tarihi", "").strip(),
    }
    if not all(form_verisi.values()):
        return form_verisi, "Tüm alanlar doldurulmalıdır."
    try:
        form_verisi["eczane_no"] = int(form_verisi["eczane_no"])
        form_verisi["ilac_no"] = int(form_verisi["ilac_no"])
        form_verisi["fiyat"] = Decimal(form_verisi["fiyat"])
        form_verisi["satis_tarihi"] = date.fromisoformat(form_verisi["satis_tarihi"])
    except (ValueError, InvalidOperation):
        return form_verisi, "Eczane, ilaç ve fiyat sayı; tarih geçerli olmalıdır."
    if form_verisi["fiyat"] < 0:
        return form_verisi, "Fiyat 0 veya daha büyük olmalıdır."
    return form_verisi, None


def _satis_hata_mesaji(hata):
    """Satis INSERT/UPDATE sirasinda olusan DB hatasini Turkce mesaja cevirir."""
    if isinstance(hata, psycopg.errors.RaiseException):
        return hata.diag.message_primary or "Satış kuralı ihlal edildi."
    if isinstance(hata, psycopg.errors.UniqueViolation):
        return "Bu eczanede aynı gün bu hastaya bu ilaç zaten satılmış."
    if isinstance(hata, psycopg.errors.ForeignKeyViolation):
        return "Seçilen eczane, hasta veya ilaç bulunamadı."
    if isinstance(hata, psycopg.errors.CheckViolation):
        return "Fiyat 0 veya daha büyük olmalıdır."
    return "Satış kaydedilemedi, girilen bilgileri kontrol edin."


def _satis_formunu_goster(satis, duzenleme):
    return render_template(
        "eczane_satis/satis_form.html",
        satis=satis,
        duzenleme=duzenleme,
        eczaneler=tum_satirlari_getir(sql.ECZANE_SECENEKLERI),
        hastalar=tum_satirlari_getir(sql.HASTA_SECENEKLERI),
        ilaclar=tum_satirlari_getir(sql.ILAC_SECENEKLERI),
        bugun=date.today().isoformat(),
    )


@eczane_satis_bp.get("/satislar")
def satis_listele():
    satislar = tum_satirlari_getir(sql.SATIS_LISTELE)
    return render_template("eczane_satis/satis_liste.html", satislar=satislar)


@eczane_satis_bp.get("/satislar/yeni")
def satis_yeni_form():
    return _satis_formunu_goster(None, duzenleme=False)


@eczane_satis_bp.post("/satislar/yeni")
def satis_ekle():
    form_verisi, hata = _satis_formunu_oku()
    if hata:
        flash(hata, "danger")
        return _satis_formunu_goster(form_verisi, duzenleme=False)
    try:
        komut_calistir(sql.SATIS_EKLE, form_verisi)
        flash("Satış kaydı eklendi.", "success")
        return redirect(url_for("eczane_satis.satis_listele"))
    except (
        psycopg.errors.RaiseException,
        psycopg.errors.UniqueViolation,
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.CheckViolation,
    ) as db_hatasi:
        flash(_satis_hata_mesaji(db_hatasi), "danger")
        return _satis_formunu_goster(form_verisi, duzenleme=False)


@eczane_satis_bp.get("/satislar/<int:satis_id>/duzenle")
def satis_duzenle_form(satis_id):
    satis = tek_satir_getir(sql.SATIS_GETIR, {"satis_id": satis_id})
    if not satis:
        flash("Satış kaydı bulunamadı.", "warning")
        return redirect(url_for("eczane_satis.satis_listele"))
    return _satis_formunu_goster(satis, duzenleme=True)


@eczane_satis_bp.post("/satislar/<int:satis_id>/duzenle")
def satis_duzenle(satis_id):
    form_verisi, hata = _satis_formunu_oku()
    form_verisi["satis_id"] = satis_id
    if hata:
        flash(hata, "danger")
        return _satis_formunu_goster(form_verisi, duzenleme=True)
    try:
        guncellenen = komut_calistir(sql.SATIS_GUNCELLE, form_verisi)
        if guncellenen:
            flash("Satış kaydı güncellendi.", "success")
        else:
            flash("Satış kaydı bulunamadı.", "warning")
        return redirect(url_for("eczane_satis.satis_listele"))
    except (
        psycopg.errors.RaiseException,
        psycopg.errors.UniqueViolation,
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.CheckViolation,
    ) as db_hatasi:
        flash(_satis_hata_mesaji(db_hatasi), "danger")
        return _satis_formunu_goster(form_verisi, duzenleme=True)


@eczane_satis_bp.post("/satislar/<int:satis_id>/sil")
def satis_sil(satis_id):
    silinen = komut_calistir(sql.SATIS_SIL, {"satis_id": satis_id})
    if silinen:
        flash("Satış kaydı silindi.", "success")
    else:
        flash("Satış kaydı bulunamadı.", "warning")
    return redirect(url_for("eczane_satis.satis_listele"))


# --- SORGULAR ---

@eczane_satis_bp.get("/sorgular")
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
    return render_template("eczane_satis/sorgular.html", sonuclar=sonuclar)


# --- RAPOR ---

@eczane_satis_bp.get("/rapor")
def rapor():
    aylik_cirolar = tum_satirlari_getir(sql.AYLIK_CIRO_LISTELE)
    eczaneler = tum_satirlari_getir(sql.ECZANE_SECENEKLERI)

    secilen_eczane_str = request.args.get("eczane_no", "").strip()
    baslangic_str = request.args.get("baslangic", "").strip()
    bitis_str = request.args.get("bitis", "").strip()

    secilen_eczane_no = None
    secilen_eczane_ad = None
    hesaplanan_ciro = None

    if secilen_eczane_str:
        try:
            secilen_eczane_no = int(secilen_eczane_str)
            baslangic_tarihi = date.fromisoformat(baslangic_str)
            bitis_tarihi = date.fromisoformat(bitis_str)
        except ValueError:
            flash("Geçerli bir eczane ve tarih aralığı seçin.", "danger")
        else:
            try:
                sonuc = tek_satir_getir(
                    sql.ECZANE_CIRO_HESAPLA,
                    {
                        "eczane_no": secilen_eczane_no,
                        "baslangic": baslangic_tarihi,
                        "bitis": bitis_tarihi,
                    },
                )
                hesaplanan_ciro = sonuc["toplam_ciro"] if sonuc else None
                for e in eczaneler:
                    if e["eczane_no"] == secilen_eczane_no:
                        secilen_eczane_ad = e["ad"]
                        break
            except psycopg.errors.RaiseException as db_hatasi:
                flash(
                    db_hatasi.diag.message_primary or "Ciro hesaplanamadı.",
                    "danger",
                )

    return render_template(
        "eczane_satis/rapor.html",
        aylik_cirolar=aylik_cirolar,
        eczaneler=eczaneler,
        secilen_eczane_no=secilen_eczane_no,
        secilen_eczane_ad=secilen_eczane_ad,
        baslangic=baslangic_str or "2026-01-01",
        bitis=bitis_str or date.today().isoformat(),
        hesaplanan_ciro=hesaplanan_ciro,
    )