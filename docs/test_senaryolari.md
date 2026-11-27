# Test Senaryoları

Her modül sahibi kendi modülü için **3 test senaryosu** yazar (pozitif + negatif adımlarıyla).
28 Kasım çapraz testinde her üye bir sonraki modülü bu senaryolara göre test eder ve sonucu tabloya işler.

| Test eden | Test edilen modül | Durum | Not |
|---|---|---|---|
| Meltem Can | M1 – Hasta & Muayene | ⏳ | |
| Elifnur Özkaya | M2 – Doktor & Reçete | ⏳ | |
| Altyn Baktybekova | M3 – Eczane & Satış | ⏳ | |
| Rojin Topuz | M4 – İlaç & Tedarik | ⏳ | |

Durum: ✅ geçti · ❌ hata bulundu (Issue numarası nota yazılır) · ⏳ test edilmedi

---

## Modül 1: Hasta & Muayene Test Senaryoları (Rojin Topuz)

*(Rojin ekleyecek: TS-M1-01, TS-M1-02, TS-M1-03)*

---

## Modül 2: Doktor & Reçete Test Senaryoları (Meltem Can)

*(Meltem ekleyecek: TS-M2-01, TS-M2-02, TS-M2-03)*

---

## Modül 3: Eczane & Satış Test Senaryoları (Elifnur Özkaya)

### TS-M3-01: Reçetesiz veya Reçete Tarihinden Önce İlaç Satışının Engellenmesi (`trg_satis_recete_kontrol`)
* **İlgili Nesne:** `satis` tablosu, `trg_satis_recete_kontrol` tetikleyicisi (`trgf_satis_recete_kontrol()`)
* **Ön Koşul:** Sistemde kayıtlı bir eczane (`eczane_no = 1`), hasta (`hasta_kimlik_no = '10000000001'`) ve ilaç (`ilac_no = 1`) bulunmalıdır.
* **Test Adımları:**
  1. **Negatif Test:** İlgili hasta ve ilaç için `recete` tablosunda kayıt yokken (veya `recete_tarihi > satis_tarihi` olacak şekilde) `/eczane-satis/satislar/yeni` formundan yeni satış kaydı eklemeye çalışın.
  2. **Pozitif Test:** İlgili hasta ve ilaç için `recete_tarihi <= satis_tarihi` koşulunu sağlayan geçerli bir reçete varken aynı satış kaydını ekleyin.
* **Beklenen Sonuç:**
  1. Negatif testte veritabanı tetikleyicisi işlemi `RAISE EXCEPTION` ile durdurur, `satis` tablosuna kayıt eklenmez ve arayüzde kırmızı uyarı (`flash`) mesajı gösterilir.
  2. Pozitif testte satış kaydı başarıyla oluşturulur ve `/eczane-satis/satislar` listesinde görüntülenir.

---

### TS-M3-02: Eczane Telefon Numarası Format ve Tekillik Doğrulaması
* **İlgili Nesne:** `eczane_telefon` tablosu (`ck_eczane_telefon_telefon_no`, `pk_eczane_telefon`)
* **Ön Koşul:** `eczane` tablosunda en az bir eczane kaydı mevcut olmalıdır.
* **Test Adımları:**
  1. **Negatif Test 1 (Format Hatası):** `/eczane-satis/telefonlar/yeni` ekranından `0` ile başlamayan veya 11 haneli olmayan bir numara (ör. `224123456` veya `abc12345678`) girerek kaydetmeye çalışın.
  2. **Negatif Test 2 (Tekrarlı Kayıt):** Aynı eczane için veritabanında zaten var olan bir telefon numarasını tekrar eklemeye çalışın.
  3. **Pozitif Test:** `0` ile başlayan 11 haneli yeni bir numara (ör. `02249998877`) girerek kaydedin.
* **Beklenen Sonuç:**
  1. Format hatasında `CHECK (telefon_no ~ '^0[0-9]{10}$')` kısıtı devreye girer ve arayüzde format uyarısı gösterilir.
  2. Tekrarlı kayıtta bileşik birincil anahtar (`pk_eczane_telefon`) çakışması yakalanır ve mükerrer kayıt uyarısı verilir.
  3. Geçerli numara `eczane_telefon` tablosuna eklenir ve telefon listesinde görünür.

---

### TS-M3-03: Satışı Olan Eczanenin Silinmesinin Engellenmesi ve Kaskad Telefon Silme
* **İlgili Nesne:** `eczane`, `eczane_telefon`, `satis` tabloları (`fk_satis_eczane`, `fk_eczane_telefon_eczane`)
* **Ön Koşul:** `eczane_telefon` tablosunda telefon numaraları bulunan iki eczaneden birinin (`Eczane A`) `satis` tablosunda kaydı bulunmalı, diğerinin (`Eczane B`) ise satış kaydı bulunmamalıdır.
* **Test Adımları:**
  1. `/eczane-satis/eczaneler` sayfasından satış kaydı bulunan `Eczane A` için **Sil** butonuna tıklayın.
  2. Satış kaydı bulunmayan `Eczane B` için **Sil** butonuna tıklayın ve ardından `/eczane-satis/telefonlar` sayfasını kontrol edin.
* **Beklenen Sonuç:**
  1. `fk_satis_eczane` (`ON DELETE RESTRICT`) kısıtı nedeniyle `Eczane A` silinemez ve arayüzde *"Bu eczaneye ait satış veya tedarik kaydı olduğu için silinemez."* uyarı mesajı görüntülenir.
  2. `Eczane B` silinir ve `fk_eczane_telefon_eczane` (`ON DELETE CASCADE`) kuralı gereği `Eczane B`'ye ait tüm telefon numaraları `eczane_telefon` tablosundan otomatik olarak temizlenir.

---

## Modül 4: İlaç & Tedarik Test Senaryoları (Altyn Baktybekova)

### TS-M4-01: Tedarik Değişikliklerinin Denetim Tablosuna Loglanması (`trg_tedarik_denetim`)
* **İlgili Nesne:** `tedarik` ve `tedarik_denetim` tabloları, `trg_tedarik_denetim` tetikleyicisi (`trgf_tedarik_denetim()`)
* **Ön Koşul:** Sistemde en az bir tedarikçi, eczane ve ilaç kaydı bulunmalıdır.
* **Test Adımları:**
  1. `/ilac-tedarik/tedarikler/yeni` formundan yeni bir tedarik ekleyin (ör. miktar `40`).
  2. Eklenen tedarikin **Düzenle** ekranından miktarı `55` yapıp kaydedin.
  3. Aynı tedarik kaydını **Sil** butonuyla silin.
  4. Her adımdan sonra `/ilac-tedarik/rapor` sayfasındaki *Son Tedarik Değişiklikleri* tablosunu kontrol edin.
* **Beklenen Sonuç:**
  1. Ekleme sonrası `tedarik_denetim` tablosuna `INSERT` kaydı düşer (eski miktar boş, yeni miktar `40`).
  2. Güncelleme sonrası `UPDATE` kaydı düşer (eski `40`, yeni `55`).
  3. Silme sonrası `DELETE` kaydı düşer (eski `55`, yeni boş). Tedarik silinse de log kayıtları kalır (`tedarik_id` bilerek FK değildir).

---

### TS-M4-02: Tedarik Kayıt Kısıtlarının Doğrulanması (miktar, tekillik, yabancı anahtar)
* **İlgili Nesne:** `tedarik` tablosu (`ck_tedarik_miktar`, `uq_tedarik_tedarikci_eczane_ilac_tarih`, `fk_tedarik_*`)
* **Ön Koşul:** `tedarikci`, `eczane` ve `ilac` tablolarında kayıt bulunmalıdır.
* **Test Adımları:**
  1. **Negatif Test 1 (Miktar):** `/ilac-tedarik/tedarikler/yeni` formunda miktarı `0` girerek kaydetmeye çalışın.
  2. **Negatif Test 2 (Tekrarlı Kayıt):** Aynı tedarikçi, eczane, ilaç ve tarihle ikinci bir tedarik eklemeye çalışın.
  3. **Pozitif Test:** Aynı kaydı farklı bir tarihle ekleyin.
* **Beklenen Sonuç:**
  1. `CHECK (miktar > 0)` kısıtı devreye girer, kayıt eklenmez ve *"Miktar 0'dan büyük olmalıdır."* uyarısı gösterilir.
  2. `UNIQUE` kısıtı çakışmayı yakalar ve *"Aynı tedarikçi, aynı gün, aynı eczaneye bu ilacı zaten getirmiş."* uyarısı gösterilir.
  3. Farklı tarihli kayıt başarıyla eklenir ve tedarik listesinde görünür.

---

### TS-M4-03: Stok Hesaplama Fonksiyonu ve Kullanılan İlacın Silinmesinin Engellenmesi (`fn_eczane_ilac_stok`)
* **İlgili Nesne:** `fn_eczane_ilac_stok(p_eczane_no, p_ilac_no)` fonksiyonu, `ilac` tablosu (`fk_tedarik_ilac`, `ON DELETE RESTRICT`)
* **Ön Koşul:** Örnek veriler yüklenmiş olmalıdır (`Merkez Şifa Eczanesi` için `Parol 500 mg Tablet` tedariki mevcut).
* **Test Adımları:**
  1. **Pozitif Test:** `/ilac-tedarik/rapor` sayfasında *Eczane Stok Sorgulama* bölümünden `Merkez Şifa Eczanesi` ve `Parol 500 mg Tablet` seçip **Hesapla**'ya basın. Sonucu, bu eczaneye gelen tedarik toplamı eksi bu ilacın satış sayısıyla karşılaştırın.
  2. **Negatif Test 1 (Fonksiyon Hatası):** Adres çubuğuna `/ilac-tedarik/rapor?eczane_no=999&ilac_no=1` yazarak olmayan bir eczane için hesaplatın.
  3. **Negatif Test 2 (Silme Kısıtı):** `/ilac-tedarik/ilaclar` sayfasından tedarik kaydı bulunan `Parol 500 mg Tablet` için **Sil** butonuna tıklayın.
* **Beklenen Sonuç:**
  1. Fonksiyon `toplam tedarik − satış sayısı` değerini döndürür (her satış 1 kutu) ve sonuç yeşil kutuda gösterilir.
  2. Fonksiyon `RAISE EXCEPTION` ile durur ve arayüzde *"Eczane bulunamadı: 999"* uyarısı gösterilir.
  3. `ON DELETE RESTRICT` nedeniyle ilaç silinmez ve *"Bu ilaca ait reçete, satış veya tedarik kaydı olduğu için silinemez."* uyarısı gösterilir.
