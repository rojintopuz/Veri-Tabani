# Test Senaryoları

Her modül sahibi kendi modülü için **3 test senaryosu** yazar (pozitif + negatif adımlarıyla).
28 Kasım çapraz testinde her üye bir sonraki modülü bu senaryolara göre test eder ve sonucu tabloya işler.

| Test eden | Test edilen modül | Durum | Not |
|---|---|---|---|
| Meltem Can | M1 – Hasta & Muayene | ⏳ | |
| Elifnur Özkaya | M2 – Doktor & Reçete | ✅ | TS-M2-01, TS-M2-02, TS-M2-03 adımları doğrulandı. |
| Altyn Baktybekova | M3 – Eczane & Satış | ⏳ | |
| Rojin Topuz | M4 – İlaç & Tedarik | ⏳ | |

Durum: ✅ geçti · ❌ hata bulundu (Issue numarası nota yazılır) · ⏳ test edilmedi

---

## Modül 1: Hasta & Muayene Test Senaryoları (Rojin Topuz)

### TS-M1-01: Gelecek Tarihli Muayenenin Engellenmesi (`trg_muayene_tarih_kontrol`)
* **İlgili Nesne:** `muayene` tablosu, `trg_muayene_tarih_kontrol` tetikleyicisi (`trgf_muayene_tarih_kontrol()`)
* **Ön Koşul:** Örnek veriler yüklü olmalıdır. `Selin Aksoy` (`'22456789034'`) hiç muayene olmamıştır; `Dr. Mehmet Öztürk` `doktor_no = 3`'tür.
* **Test Adımları:**
  1. **Negatif Test 1 (Ekleme):** `/hasta-muayene/muayeneler/yeni` formundan Selin Aksoy → Dr. Mehmet Öztürk, tarih olarak **yarının tarihi** ile muayene eklemeye çalışın.
  2. **Negatif Test 2 (Düzenleme):** Var olan bir muayeneyi `/hasta-muayene/muayeneler/<no>/duzenle` ekranından açıp tarihini yarına alarak kaydetmeye çalışın.
  3. **Pozitif Test:** Aynı muayeneyi **bugünün tarihi** ile ekleyin.
* **Beklenen Sonuç:**
  1. Negatif testlerde tetikleyici `RAISE EXCEPTION` ile işlemi durdurur, `muayene` tablosu değişmez, form girilen değerlerle yeniden açılır ve *"Muayene tarihi gelecekte olamaz."* uyarısı gösterilir.
  2. Pozitif testte muayene eklenir, `/hasta-muayene/muayeneler` listesinde görünür ve Selin Aksoy `/hasta-muayene/rapor` sayfasındaki özette 1 muayeneyle listelenir.

> Not: Formdaki tarih kutusu tarayıcıda da gelecek tarihi engeller (`max`). Tetikleyicinin kendisini denemek için tarayıcıda kutuyu elle değiştirmek ya da SQL'den denemek gerekir:
> `INSERT INTO muayene (doktor_no, hasta_kimlik_no, muayene_tarihi) VALUES (3, '22456789034', CURRENT_DATE + 1);`

---

### TS-M1-02: Hasta Kimlik No, Ad ve Yaş Kısıtlarının Doğrulanması
* **İlgili Nesne:** `hasta` tablosu (`pk_hasta`, `ck_hasta_kimlik_no`, `ck_hasta_ad`, `ck_hasta_yas`)
* **Ön Koşul:** `Ayşe Yılmaz` (`'10234567810'`) kayıtlıdır.
* **Test Adımları:** `/hasta-muayene/hastalar/yeni` formundan sırayla:
  1. **Negatif Test 1 (Format):** Kimlik no `01234567890` (0 ile başlıyor) veya `1234` (11 hane değil) girin.
  2. **Negatif Test 2 (Tekrar):** Kimlik no `10234567810` (Ayşe Yılmaz'ınki) girin.
  3. **Negatif Test 3 (Boş ad):** Ad alanına sadece boşluk girin.
  4. **Negatif Test 4 (Yaş):** Yaş olarak `200` girin.
  5. **Pozitif Test:** Kimlik no `30000000001`, ad `Test Hasta`, yaş `40` ile kaydedin.
* **Beklenen Sonuç:**
  1. Her negatif testte kayıt eklenmez, form girilen değerlerle yeniden açılır ve ilgili Türkçe uyarı gösterilir: format → *"Kimlik no 11 haneli olmalı ve 0 ile başlamamalıdır."*, tekrar → *"Bu kimlik numarasıyla kayıtlı bir hasta zaten var."* (`pk_hasta`), boş ad → *"Hasta adı boş bırakılamaz."*, yaş → *"Yaş 0 ile 130 arasında olmalıdır."*
  2. Pozitif testte hasta eklenir ve `/hasta-muayene/hastalar` listesinde görünür.
  3. Düzenleme ekranında kimlik no alanı salt okunurdur (birincil anahtar değiştirilemez).

---

### TS-M1-03: Kaydı Olan Hastanın Silinmesinin Engellenmesi ve Muayene Geçmişi Fonksiyonu
* **İlgili Nesne:** `hasta`, `muayene`, `recete`, `satis` tabloları (`fk_muayene_hasta`, `fk_recete_hasta`, `fk_satis_hasta`, `ON DELETE RESTRICT`); `fn_hasta_muayene_gecmisi(p_hasta_kimlik_no)`; `vw_hasta_muayene_ozeti`
* **Ön Koşul:** `Hatice Doğan`'ın (`'18012345696'`) 3 muayenesi vardır; TS-M1-02'de eklenen `Test Hasta`'nın (`'30000000001'`) hiçbir kaydı yoktur.
* **Test Adımları:**
  1. `/hasta-muayene/hastalar` sayfasında Hatice Doğan için **Sil** butonuna tıklayın.
  2. Aynı satırdaki **Geçmiş** butonuna tıklayın (veya `/hasta-muayene/rapor` sayfasında Hatice Doğan'ı seçip **Göster**'e basın).
  3. Test Hasta için **Sil** butonuna tıklayın.
* **Beklenen Sonuç:**
  1. `ON DELETE RESTRICT` nedeniyle Hatice Doğan silinmez ve *"Bu hastanın muayene, reçete veya satış kaydı olduğu için silinemez."* uyarısı gösterilir.
  2. Fonksiyon Hatice Doğan'ın 3 muayenesini doktor adı ve uzmanlık alanıyla, en yeniden eskiye listeler; özet tablosunda (görünüm) 3 muayene ve 3 farklı doktor görünür.
  3. Test Hasta silinir ve listeden kalkar. Muayenesi olmayan bir hasta rapor sayfasında seçilirse *"Bu hasta henüz muayene olmamış."* mesajı gösterilir.

---

## Modül 2: Doktor & Reçete Test Senaryoları (Meltem Can)

### TS-M2-01: Muayenesiz veya Muayeneden Önce Reçete Yazılmasının Engellenmesi (`trg_recete_muayene_kontrol`)
* **İlgili Nesne:** `recete` tablosu, `trg_recete_muayene_kontrol` tetikleyicisi (`trgf_recete_muayene_kontrol()`)
* **Ön Koşul:** Örnek veriler yüklü olmalıdır. `Dr. Ali Yılmaz` (`doktor_no = 1`), `Ayşe Yılmaz`'ı (`'10234567810'`) 02.09.2026'da muayene etmiştir; `Dr. Oğuz Tekin` (`doktor_no = 11`) hiç muayene yapmamıştır.
* **Test Adımları:**
  1. **Negatif Test 1 (Muayene yok):** `/doktor-recete/receteler/yeni` formundan Dr. Oğuz Tekin → Ayşe Yılmaz → Parol 500 mg, tarih 01.11.2026 ile reçete eklemeye çalışın.
  2. **Negatif Test 2 (Muayeneden önce):** Dr. Ali Yılmaz → Ayşe Yılmaz → Parol 500 mg, tarih **01.09.2026** (muayeneden bir gün önce) ile reçete eklemeye çalışın.
  3. **Pozitif Test:** Aynı reçeteyi tarih **02.09.2026** (muayene günü) ile ekleyin.
* **Beklenen Sonuç:**
  1. Negatif testlerde tetikleyici `RAISE EXCEPTION` ile işlemi durdurur, `recete` tablosuna kayıt eklenmez, form girilen değerlerle yeniden açılır ve kırmızı uyarı (`flash`) mesajı gösterilir.
  2. Pozitif testte reçete eklenir ve `/doktor-recete/receteler` listesinde görünür. (Bir reçetenin tarihi düzenlenip muayeneden önceye alınmak istenirse de aynı tetikleyici devreye girer.)

---

### TS-M2-02: Muayenesi veya Reçetesi Olan Doktorun Silinmesinin Engellenmesi
* **İlgili Nesne:** `doktor`, `muayene`, `recete` tabloları (`fk_muayene_doktor`, `fk_recete_doktor`, `ON DELETE RESTRICT`)
* **Ön Koşul:** `Dr. Ali Yılmaz`'ın (`doktor_no = 1`) muayene ve reçete kayıtları vardır; `Dr. Deniz Uçar`'ın (`doktor_no = 12`) hiçbir kaydı yoktur.
* **Test Adımları:**
  1. `/doktor-recete/doktorlar` sayfasında Dr. Ali Yılmaz için **Sil** butonuna tıklayın.
  2. Dr. Deniz Uçar için **Sil** butonuna tıklayın.
* **Beklenen Sonuç:**
  1. `ForeignKeyViolation` yakalanır, doktor silinmez ve *"Bu doktorun muayene veya reçete kaydı olduğu için silinemez."* uyarısı gösterilir.
  2. Dr. Deniz Uçar silinir, *"Doktor silindi."* mesajı görünür ve doktor listeden kalkar.

---

### TS-M2-03: Doktor ve Reçete Formlarında Kısıt Doğrulaması
* **İlgili Nesne:** `ck_doktor_deneyim_yili`, `ck_recete_miktar`, `uq_recete_doktor_hasta_ilac_tarih`
* **Ön Koşul:** Örnek veriler yüklü olmalıdır.
* **Test Adımları:**
  1. **Negatif Test 1:** `/doktor-recete/doktorlar/yeni` formunda ad alanına sadece boşluk yazıp kaydetmeye çalışın.
  2. **Negatif Test 2:** Deneyim yılına `70` girip kaydetmeye çalışın.
  3. **Negatif Test 3 (Tekrarlı reçete):** Dr. Ali Yılmaz → Ayşe Yılmaz → Parol 500 mg, tarih 03.09.2026 reçetesini (örnek veride zaten var) tekrar ekleyin.
  4. **Pozitif Test:** `Dr. Test Doktor`, `Nöroloji`, `5` yıl ile yeni doktor ekleyin.
* **Beklenen Sonuç:**
  1. Boş ad kaydedilmez, *"Doktor adı ve uzmanlık alanı boş bırakılamaz."* uyarısı gösterilir.
  2. Deneyim yılı 0–65 aralığı dışında olduğu için kayıt yapılmaz ve uyarı gösterilir.
  3. `UniqueViolation` yakalanır, *"Bu doktor aynı gün bu hastaya bu ilacı zaten reçete etmiş."* uyarısı gösterilir.
  4. Yeni doktor eklenir ve listenin sonunda görünür.

---

## Modül 3: Eczane & Satış Test Senaryoları (Elifnur Özkaya)

### TS-M3-01: Reçetesiz veya Reçete Tarihinden Önce İlaç Satışının Engellenmesi (`trg_satis_recete_kontrol`)
* **İlgili Nesne:** `satis` tablosu, `trg_satis_recete_kontrol` tetikleyicisi (`trgf_satis_recete_kontrol()`)
* **Ön Koşul:** Örnek veriler yüklü olmalıdır. Sistemde kayıtlı bir eczane (`eczane_no = 1`), hasta (`Ayşe Yılmaz` — `'10234567810'`) ve ilaç (`ilac_no = 1`) bulunmalıdır.
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
* **Ön Koşul:** Örnek veriler yüklü olmalıdır (`eczane_no = 1` kaydının satış/tedarik ilişkisi vardır).
* **Test Adımları:**
  1. `/eczane-satis/eczaneler/yeni` ekranından `Test Eczanesi` adıyla yeni bir eczane ekleyin ve `/eczane-satis/telefonlar/yeni` ekranından bu eczaneye `02248887766` telefon numarasını tanımlayın.
  2. `/eczane-satis/eczaneler` sayfasından satış kaydı bulunan mevcut eczane (`eczane_no = 1`) için **Sil** butonuna tıklayın.
  3. Yeni eklediğiniz `Test Eczanesi` için **Sil** butonuna tıklayın ve ardından `/eczane-satis/telefonlar` sayfasını kontrol edin.
* **Beklenen Sonuç:**
  1. Yeni eczane ve telefon numarası listelere eklenir.
  2. `ON DELETE RESTRICT` kısıtı nedeniyle mevcut eczane silinemez ve arayüzde *"Bu eczaneye ait satış veya tedarik kaydı olduğu için silinemez."* uyarı mesajı görüntülenir.
  3. `Test Eczanesi` silinir ve `fk_eczane_telefon_eczane` (`ON DELETE CASCADE`) kuralı gereği `02248887766` numarası `eczane_telefon` tablosundan otomatik olarak temizlenir.

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