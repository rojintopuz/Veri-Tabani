# Katkı Kuralları

Bu repoya kod, SQL veya doküman ekleyen herkes bu kurallara uyar. Kurallara uymayan PR birleştirilmez.

**Temel kural: her dosyanın tek sahibi vardır** (bkz. [`.github/CODEOWNERS`](.github/CODEOWNERS)). Başkasının dosyasında değişiklik gerekiyorsa sahibine Issue açılır veya sahibinin onayıyla PR gönderilir. Herkes kendi dosyasında çalıştığı için birleştirme çakışması (merge conflict) neredeyse hiç yaşanmaz.

## İçindekiler
1. [Adlandırma kuralları](#1-adlandırma-kuralları)
2. [SQL yazım standardı](#2-sql-yazım-standardı)
3. [Python / Flask standardı](#3-python--flask-standardı)
4. [Git iş akışı](#4-git-iş-akışı)
5. [Parçalar nasıl birleşiyor?](#5-parçalar-nasıl-birleşiyor)

---

## 1. Adlandırma kuralları

### 1.1 Genel
- **Dil:** Türkçe, ama **sadece ASCII**: `ı→i, ş→s, ğ→g, ü→u, ö→o, ç→c`. (`ilac`, `recete`, `satis`, `tedarikci`.)
  Bu kural tablo, kolon, değişken, fonksiyon, dosya ve dal adlarının hepsi için geçerli.
- Kullanıcının **ekranda gördüğü** metinler (HTML, flash mesajları, rapor) düzgün Türkçe karakterlerle yazılır: "İlaç Listesi", "Reçete eklendi".
- Kısaltma yok: `hst`, `dr`, `tel` değil → `hasta`, `doktor`, `telefon_no`.

### 1.2 Veritabanı nesneleri

| Nesne | Kural | Örnek |
|---|---|---|
| Şema | `eczane` | |
| Tablo | tekil, küçük harf, `snake_case` | `hasta`, `eczane_telefon` |
| Varlık PK | `<tablo>_no` (hasta için `hasta_kimlik_no`) | `doktor_no`, `ilac_no` |
| İlişki tablosu PK | `<tablo>_id` | `muayene_id`, `satis_id` |
| FK kolonu | Referans verdiği PK ile **birebir aynı ad** | `recete.doktor_no → doktor.doktor_no` |
| Tarih kolonu | `<olay>_tarihi` | `muayene_tarihi`, `satis_tarihi` |
| Diğer kolonlar | önek yok, `snake_case` | `ad`, `adres`, `uzmanlik_alani` |
| PK kısıtı | `pk_<tablo>` | `pk_hasta` |
| FK kısıtı | `fk_<tablo>_<hedef_tablo>` | `fk_recete_ilac` |
| UNIQUE | `uq_<tablo>_<kolonlar>` | `uq_muayene_doktor_hasta_tarih` |
| CHECK | `ck_<tablo>_<kolon>` | `ck_hasta_yas` |
| Index | `idx_<tablo>_<kolon>` | `idx_satis_satis_tarihi` |
| View | `vw_<konu>` | `vw_eczane_aylik_ciro` |
| Fonksiyon | `fn_<fiil/konu>` | `fn_eczane_ciro` |
| Fonksiyon parametresi | `p_<ad>` | `p_eczane_no`, `p_baslangic` |
| PL/pgSQL yerel değişken | `v_<ad>` | `v_toplam_miktar` |
| Trigger | `trg_<tablo>_<amac>` | `trg_satis_recete_kontrol` |
| Trigger fonksiyonu | `trgf_<tablo>_<amac>` | `trgf_satis_recete_kontrol` |
| JOIN'de tablo takma adı | tablonun ilk harf(ler)i | `h`=hasta, `d`=doktor, `m`=muayene, `r`=recete, `i`=ilac, `e`=eczane, `s`=satis, `tc`=tedarikci, `t`=tedarik |

> `ad` gibi ortak kolonlar JOIN'li sorgularda **mutlaka** `AS` ile yeniden adlandırılır: `h.ad AS hasta_ad, d.ad AS doktor_ad`.

### 1.3 Python

| Öğe | Kural | Örnek |
|---|---|---|
| Değişken, fonksiyon | `snake_case`, Türkçe-ASCII | `hasta_listesi`, `hasta_ekle()` |
| Sınıf | `PascalCase` | `HastaFormu` |
| Sabit, SQL metni | `BUYUK_HARF_SNAKE` | `HASTA_LISTELE`, `VERITABANI_SEMASI` |
| Dosya / paket | `snake_case` | `sorgular.py`, `hasta_muayene/` |
| Blueprint nesnesi | `<modul>_bp` | `hasta_muayene_bp` |
| Blueprint adı | `<modul>` | `"hasta_muayene"` |
| Route fonksiyonu | `<tablo>_<eylem>` (eylemler: `listele`, `ekle`, `duzenle`, `sil`); modül geneli için `rapor`, `sorgular` | `recete_duzenle`, `sorgular` |
| Şablon | `templates/<modul>/<tablo>_<sayfa>.html` (sayfalar: `liste`, `form`); modül geneli: `rapor.html`, `sorgular.html` | `doktor_recete/recete_form.html` |
| HTML form alanı `name` | DB kolon adıyla birebir aynı | `name="hasta_kimlik_no"` |

### 1.4 URL düzeni

| İşlem | Yöntem | URL |
|---|---|---|
| Listele | GET | `/<modul-tireli>/<tablo>` → `/hasta-muayene/hastalar` |
| Yeni kayıt formu / kaydet | GET / POST | `/hasta-muayene/hastalar/yeni` |
| Düzenle | GET / POST | `/hasta-muayene/hastalar/<anahtar>/duzenle` |
| Sil | **sadece POST** | `/hasta-muayene/hastalar/<anahtar>/sil` |
| Rapor | GET | `/hasta-muayene/rapor` |
| Sorgular | GET | `/hasta-muayene/sorgular` |

URL ön ekleri: `/hasta-muayene`, `/doktor-recete`, `/eczane-satis`, `/ilac-tedarik`.

---

---

## 2. SQL yazım standardı

- Hedef: **PostgreSQL 15+**. Sadece standart Postgres özellikleri.
- Anahtar kelimeler **BÜYÜK** (`SELECT`, `CREATE TABLE`), isimler **küçük**.
- 4 boşluk girinti, her kolon ayrı satırda, her dosyanın sonunda `;`.
- Kısıtlar kolon satırına değil, tablonun sonunda **isimli** `CONSTRAINT` olarak yazılır.
- `SELECT *` yasak: kolonlar tek tek yazılır.
- Her dosyanın başında başlık bloğu, her sorgunun üstünde "hangi soruya cevap veriyor" yorumu bulunur.
- Bir dosya = bir tablo (veya bir view / fonksiyon / trigger). İstisna: `eczane.sql` dosyası `eczane_telefon` tablosunu da içerir.
- Veri dosyalarında varlık tablolarına **ID yazılmaz** (otomatik 1, 2, 3… verilir). Kurulum her seferinde sıfırdan yapıldığı için ilişki tablolarında bu numaralar güvenle kullanılır.

### 2.1 Varlık tablosu şablonu — `db/10_varliklar/hasta.sql`

```sql
-- =====================================================
-- Dosya    : db/10_varliklar/hasta.sql
-- Modul    : M1 - Hasta & Muayene
-- Sahibi   : Rojin Topuz (032390078)
-- Aciklama : Hasta varlik tablosu
-- =====================================================
CREATE TABLE hasta (
    hasta_kimlik_no  CHAR(11)      NOT NULL,
    ad               VARCHAR(100)  NOT NULL,
    adres            VARCHAR(250),
    yas              SMALLINT      NOT NULL,
    CONSTRAINT pk_hasta PRIMARY KEY (hasta_kimlik_no),
    CONSTRAINT ck_hasta_kimlik_no CHECK (hasta_kimlik_no ~ '^[1-9][0-9]{10}$'),
    CONSTRAINT ck_hasta_yas CHECK (yas BETWEEN 0 AND 130)
);
```

### 2.2 İlişki tablosu şablonu — `db/20_iliskiler/muayene.sql`

```sql
CREATE TABLE muayene (
    muayene_id       INTEGER   GENERATED BY DEFAULT AS IDENTITY,
    doktor_no        INTEGER   NOT NULL,
    hasta_kimlik_no  CHAR(11)  NOT NULL,
    muayene_tarihi   DATE      NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pk_muayene PRIMARY KEY (muayene_id),
    CONSTRAINT fk_muayene_doktor FOREIGN KEY (doktor_no)
        REFERENCES doktor (doktor_no) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_muayene_hasta FOREIGN KEY (hasta_kimlik_no)
        REFERENCES hasta (hasta_kimlik_no) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_muayene_doktor_hasta_tarih UNIQUE (doktor_no, hasta_kimlik_no, muayene_tarihi)
);

CREATE INDEX idx_muayene_hasta_kimlik_no ON muayene (hasta_kimlik_no);
```

### 2.3 Trigger şablonu — `db/50_tetikleyiciler/m1_trg_muayene_tarih_kontrol.sql`

```sql
CREATE OR REPLACE FUNCTION trgf_muayene_tarih_kontrol()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.muayene_tarihi > CURRENT_DATE THEN
        RAISE EXCEPTION 'Muayene tarihi gelecekte olamaz: %', NEW.muayene_tarihi;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_muayene_tarih_kontrol
BEFORE INSERT OR UPDATE ON muayene
FOR EACH ROW
EXECUTE FUNCTION trgf_muayene_tarih_kontrol();
```

### 2.4 Sorgu dosyası şablonu — `db/sorgular/m1_hasta_muayene.sql`

```sql
-- -----------------------------------------------------
-- S1 (a - 3 tablolu JOIN)
-- Soru : Her muayenede hangi hasta hangi doktora gitmis?
-- -----------------------------------------------------
SELECT
    m.muayene_id,
    h.ad  AS hasta_ad,
    d.ad  AS doktor_ad,
    d.uzmanlik_alani,
    m.muayene_tarihi
FROM muayene AS m
JOIN hasta   AS h ON h.hasta_kimlik_no = m.hasta_kimlik_no
JOIN doktor  AS d ON d.doktor_no       = m.doktor_no
ORDER BY m.muayene_tarihi DESC;
```

### 2.5 Veri dosyası sıralaması (önemli)

Trigger'lar veriden **önce** kurulur, yani örnek veriler iş kurallarına uymak zorundadır. Bu yüzden veri zinciri sırayla yazılır:

`11–15 varlık verileri` → `21_muayene (M1)` → `22_recete (M2: sadece muayenesi olan doktor-hasta çiftleri)` → `23_satis (M3: sadece reçetesi olan hasta-ilaç çiftleri)` → `24_tedarik (M4)`

---

---

## 3. Python / Flask standardı


**Kesin kurallar:**
1. Veritabanına **sadece** `app/db.py` üzerinden bağlanılır. Başka yerde `psycopg.connect` yazılmaz.
2. SQL metinleri sadece modülün `sorgular.py` dosyasında, sabit olarak durur.
3. **SQL'e asla f-string / `+` ile değer eklenmez** (SQL injection). Her zaman parametre kullanılır: `%(ad)s`.
4. DB hataları (`UniqueViolation`, `CheckViolation`, `ForeignKeyViolation`, trigger'dan gelen `RaiseException`) yakalanır ve kullanıcıya `flash` ile anlaşılır Türkçe mesaj gösterilir.
5. Silme işlemi sadece POST ile yapılır.
6. Herkes `base.html` şablonunu genişletir (`{% extends "base.html" %}`); kendi CSS'ini yazmaz, Bootstrap sınıflarını kullanır.
7. Biçim: PEP 8, 4 boşluk, satır ≤ 100 karakter.


### 3.1 Veritabanı yardımcıları (`app/db.py`)

Modüller veritabanına sadece şu üç fonksiyonla erişir:

| Fonksiyon | Ne döndürür | Kullanım |
|---|---|---|
| `tum_satirlari_getir(sql, parametreler=None)` | Satır listesi (her satır `dict`) | Listeleme, rapor, sorgular |
| `tek_satir_getir(sql, parametreler=None)` | Tek satır (`dict`) veya `None` | Düzenleme formunu doldurma |
| `komut_calistir(sql, parametreler=None)` | Etkilenen satır sayısı | INSERT / UPDATE / DELETE |

Bağlantı `eczane` şemasına ayarlıdır; blok hatasız biterse `COMMIT`, hata olursa `ROLLBACK` yapılır.

### 3.2 Modül şablonu (örnek: M1)


`app/moduller/hasta_muayene/__init__.py`
```python
from flask import Blueprint

hasta_muayene_bp = Blueprint("hasta_muayene", __name__, url_prefix="/hasta-muayene")

from . import routes  # noqa: E402,F401  (blueprint olustuktan sonra import edilmeli)
```

`app/moduller/hasta_muayene/sorgular.py`
```python
"""M1 - Hasta & Muayene modulunun SQL metinleri."""

HASTA_LISTELE = """
    SELECT hasta_kimlik_no, ad, adres, yas
    FROM hasta
    ORDER BY ad;
"""

HASTA_EKLE = """
    INSERT INTO hasta (hasta_kimlik_no, ad, adres, yas)
    VALUES (%(hasta_kimlik_no)s, %(ad)s, %(adres)s, %(yas)s);
"""
```

`app/moduller/hasta_muayene/routes.py`
```python
import psycopg
from flask import flash, redirect, render_template, request, url_for

from app.db import komut_calistir, tum_satirlari_getir

from . import hasta_muayene_bp
from . import sorgular as sql


@hasta_muayene_bp.get("/hastalar")
def hasta_listele():
    hastalar = tum_satirlari_getir(sql.HASTA_LISTELE)
    return render_template("hasta_muayene/hasta_liste.html", hastalar=hastalar)


@hasta_muayene_bp.post("/hastalar/yeni")
def hasta_ekle():
    form_verisi = {
        "hasta_kimlik_no": request.form["hasta_kimlik_no"].strip(),
        "ad": request.form["ad"].strip(),
        "adres": request.form.get("adres", "").strip() or None,
        "yas": int(request.form["yas"]),
    }
    try:
        komut_calistir(sql.HASTA_EKLE, form_verisi)
        flash("Hasta eklendi.", "success")
    except psycopg.errors.UniqueViolation:
        flash("Bu kimlik numarasıyla kayıtlı hasta zaten var.", "danger")
    except psycopg.errors.CheckViolation:
        flash("Kimlik no 11 haneli olmalı, yaş 0-130 arasında olmalı.", "danger")
    return redirect(url_for("hasta_muayene.hasta_listele"))
```

`run.py`
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

---

---

## 4. Git iş akışı

- `main` korumalı: doğrudan push **yok**, her değişiklik Pull Request ile girer, **1 onay** şart (onaylayan: aşağıdaki inceleme tablosu).
- Her iş = 1 Issue = 1 dal = 1 PR. PR'lar küçük olsun (ideali tek tablo / tek sayfa).
- Birleştirme yöntemi: **Squash and merge**.
- Dalda çalışmaya başlamadan önce: `git pull origin main`.

**Dal adı:** `<isim>/<modul>-<konu>` → `rojin/m1-hasta-ddl`, `altyn/m4-tedarik-trigger`, `elifnur/ortak-base-html`

**Commit mesajı:** `<tip>(<kapsam>): <ne yapıldı, küçük harf, Türkçe>`

| tip | ne zaman |
|---|---|
| `feat` | yeni özellik / sayfa |
| `sql` | tablo, view, fonksiyon, trigger, veri, sorgu |
| `fix` | hata düzeltme |
| `docs` | README, rapor, diyagram |
| `refactor` | davranışı değiştirmeyen düzenleme |
| `chore` | ayar, bağımlılık, CI |

Kapsam: `m1`, `m2`, `m3`, `m4`, `db`, `app`, `ortak`.
Örnekler: `sql(m2): recete tablosu ve fk kisitlari eklendi`, `feat(m3): satis listeleme sayfasi`.

**PR kontrol listesi** (`.github/pull_request_template.md`):
```markdown
## Ne yapıldı?
- 

## Kontrol listesi
- [ ] `python scripts/db_kur.py` kendi DB'mde hatasız çalıştı
- [ ] Adlandırma kurallarına (CONTRIBUTING §1) uydum
- [ ] Sadece kendi dosyalarımı değiştirdim (değilse sahibinden onay aldım)
- [ ] SQL'de `SELECT *` ve Python'da string birleştirmeli SQL yok
- [ ] Uygulama sayfası açılıyor ve ekle/düzenle/sil denendi
- [ ] Şifre / `.env` commit edilmedi

İlgili Issue: #
```

---


**PR'ı kim inceler?**

| PR'ı açan modül | İnceleyen |
|---|---|
| M1 Hasta & Muayene | M2 sahibi |
| M2 Doktor & Reçete | M3 sahibi |
| M3 Eczane & Satış | M4 sahibi |
| M4 İlaç & Tedarik | M1 sahibi |
| Ortak dosyalar | Dosyanın CODEOWNERS sahibi |

PR'lar en geç 24 saat içinde incelenir.

---

## 5. Parçalar nasıl birleşiyor?

**Veritabanı.** `scripts/db_kur.py`, `db/` altındaki klasörleri şu sırayla çalıştırır:
`00_sema → 10_varliklar → 20_iliskiler → 30_gorunumler → 40_fonksiyonlar → 50_tetikleyiciler → 60_veriler`.
Klasör içindeki dosyalar alfabetik sırayla çalışır. Hata olursa betik **hangi dosyada** olduğunu yazıp durur. Sonunda teslim için tek parça `db/build/tam_kurulum.sql` dosyasını üretir. Yabancı anahtar bağımlılıkları klasör sırasıyla çözülür; bu yüzden bir tablo, başvurduğu tablodan önceki bir klasöre konmaz.

**Otomatik kontrol (CI).** Her PR'da GitHub Actions boş bir PostgreSQL açıp `db_kur.py` dosyasını çalıştırır. Kırmızı ✗ alan PR birleştirilmez.

**Uygulama.** Dört modülün blueprint'i `app/__init__.py` içinde baştan kayıtlıdır, menü `base.html` içinde hazırdır. Modül sahipleri sadece kendi `app/moduller/<modul>/` ve `app/templates/<modul>/` klasörlerinde çalışır; sayfa yazıldığı an menüde görünür.

**Veritabanı ortamları.** Herkes kendi geliştirme veritabanında çalışır. Ortak veritabanı (demo ve sunum için) sadece `main` dalından ve sadece altyapı sorumlusu tarafından kurulur.
