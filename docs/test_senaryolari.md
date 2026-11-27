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
