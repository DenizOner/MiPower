# MiPower — Home Assistant Özel Entegrasyonu

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower**, geleneksel Wake-on-LAN (WOL) özelliğini desteklemeyen, ancak bir Bluetooth eşleştirme isteği ile "uyandırılabilecek" medya oynatıcıların güç durumunu kontrol etmenizi sağlayan bir Home Assistant entegrasyonudur. Özellikle Xiaomi Mi Box gibi cihazlar için tasarlanmıştır, ancak benzer diğer Android TV kutularıyla da çalışabilir.

Bu entegrasyon, Home Assistant'ta bir `switch` (anahtar) varlığı (entity) oluşturur. 
- Anahtarı **AÇMAK**, cihazı uyandırmak için `bluetoothctl` aracılığıyla bir dizi Bluetooth komutu gönderir.
- Anahtarı **KAPATMAK**, bağlantılı cihaz için `media_player.turn_off` hizmetini çağırır.
- Anahtarın durumu, bağlantılı medya oynatıcı varlığının durumuyla otomatik olarak senkronize edilir.

## 🤝 Destek Olun

MiPower projesi, açık kaynak topluluğuna değer katma vizyonuyla geliştirilmektedir. Bu projenin sürekliliğini ve gelişim hızını korumak için desteğiniz hayati önem taşımaktadır.

Emeğimi takdir ediyorsanız, GitHub Sponsorlukları veya aşağıdaki platformlar üzerinden bana destek olabilirsiniz. Şimdiden teşekkürler!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatif olarak, deponun sağ üst köşesindeki **Sponsor düğmesine (❤️)** tıklayarak tüm finansman seçeneklerini görebilirsiniz.

## Ön Koşullar

- **Home Assistant OS / Supervised / Container:** Bu entegrasyon, `bluetoothctl` komut satırı aracının mevcut ve erişilebilir olduğu, Linux tabanlı bir Home Assistant kurulumu gerektirir. Windows üzerindeki Home Assistant Core kurulumunda **ÇALIŞMAZ**.

## HACS Üzerinden Kurulum (Önerilen)

Bu entegrasyon, HACS'de özel bir depo (custom repository) olarak mevcuttur.

1.  HACS kontrol panelinize gidin.
2.  **Integrations** (Entegrasyonlar) üzerine tıklayın.
3.  Sağ üst köşedeki üç nokta menüsüne tıklayın ve **"Custom repositories"** ("Özel depolar") seçeneğini seçin.
4.  İletişim kutusuna aşağıdaki bilgileri girin:
    - **Repository (Depo):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategori):** `Integration` (Entegrasyon)
5.  **"Add"** ("Ekle") üzerine tıklayın.
6.  "MiPower" entegrasyonu artık HACS listenizde görünecektir. Üzerine tıklayın.
7.  **"Download"** ("İndir") düğmesine tıklayın ve ardından sonraki pencerede tekrar **"Download"** ("İndir") üzerine tıklayın.
8.  İndirme tamamlandıktan sonra, entegrasyonun yüklenmesi için **Home Assistant'ı YENİDEN BAŞLATMALISINIZ**.

## Manuel Kurulum

HACS önerilen yöntem olsa da, entegrasyonu manuel olarak da kurabilirsiniz.

1.  Deponun [Sürümler sayfasına (Releases page)](https://github.com/DenizOner/MiPower/releases) gidin ve en son sürümdeki `mipower.zip` dosyasını indirin.
2.  İndirilen dosyayı açın.
3.  Açılan klasörün içinde bir `custom_components` dizini bulacaksınız. İçindeki `mipower` klasörünü kopyalayın.
4.  Kopyalanan `mipower` klasörünü Home Assistant yapılandırma dizininizdeki `custom_components` klasörüne yapıştırın. Eğer `custom_components` klasörü mevcut değilse, onu oluşturmanız gerekir.
    - Son yol şöyle görünmelidir: `.../config/custom_components/mipower/`
5.  Home Assistant'ı yeniden başlatın.

## Yapılandırma

Yeniden başlattıktan sonra, MiPower anahtarını ekleyebilir ve yapılandırabilirsiniz.

1.  **Settings > Devices & Services** (Ayarlar > Cihazlar ve Hizmetler) bölümüne gidin.
2.  Sağ alt köşedeki **"+ Add Integration"** ("+ Entegrasyon Ekle") düğmesine tıklayın.
3.  **"MiPower"** araması yapın ve üzerine tıklayın.

### Kolay Kurulum (Önerilen)

Bu, entegrasyonu yapılandırmanın en basit yoludur.

1.  İstendiğinde **"Easy Setup"** ("Kolay Kurulum") seçeneğini belirleyin.
2.  Entegrasyon, sisteminizdeki Bluetooth özellikli medya oynatıcıları otomatik olarak keşfedecektir.
3.  Açılır listeden hedef cihazınızı (örn. "Xiaomi Mi Box 4") seçin.
4.  **"Submit"** ("Gönder") üzerine tıklayın.

Hepsi bu kadar! Entegrasyon, medya oynatıcınıza bağlı bir anahtar oluşturacaktır.

### Gelişmiş Kurulum

Kolay Kurulum cihazınızı bulamazsa veya en baştan gelişmiş zamanlama ayarlarını yapılandırmanız gerekirse bu yöntemi kullanın.

1.  **Adım 1: Cihaz Seçimi**
    - **"Advanced Setup"** ("Gelişmiş Kurulum") seçeneğini belirleyin.
    - Home Assistant'ınızdaki *tüm* medya oynatıcıların listesinden hedef medya oynatıcınızı seçin.
2.  **Adım 2: MAC Adresi**
    - Entegrasyon, seçilen cihazın Bluetooth MAC Adresini bulmaya çalışacaktır. 
    - Bulunursa, önceden doldurulacaktır. Doğru olduğundan emin olun.
    - Bulunamazsa, cihazınızın Bluetooth MAC Adresini manuel olarak girmeniz gerekir.
3.  **Adım 3: Zamanlama Ayarları**
    - Bluetooth komutları için çeşitli zaman aşımı (timeouts) ve gecikmeler yapılandırabilirsiniz. Çoğu kullanıcı için varsayılan değerler yeterlidir.
4.  Kurulumu tamamlamak için **"Submit"** ("Gönder") üzerine tıklayın.

## Seçenekler

MiPower anahtarınızı yapılandırdıktan sonra, zamanlama ayarlarını istediğiniz zaman ayarlayabilirsiniz.

1.  **Settings > Devices & Services** (Ayarlar > Cihazlar ve Hizmetler) bölümüne gidin.
2.  MiPower entegrasyonunu bulun ve **"Configure"** ("Yapılandır") üzerine tıklayın.
3.  Gerektiğinde *debounce*, zaman aşımı ve gecikmeler için kaydırıcıları ayarlayın.

## Zamanlama Ayarlarının Açıklaması

Yapılandırma veya seçenekler menüsünde, Bluetooth komutlarının zamanlamasını hassas bir şekilde ayarlayabilirsiniz. Çoğu kullanıcı için varsayılan değerler iyi çalışır.

- **Turn-On Debounce (Açılma Titreşim Engelleme):** 'Aç' komutunun tekrar yürütülmeden önce geçmesi gereken minimum süre (saniye cinsinden). Bu, anahtar hızla açılıp kapatılırsa cihazın uyandırma sinyalleriyle spamlenmesini önler.

- **Turn-Off Debounce (Kapanma Titreşim Engelleme):** 'Kapat' komutunun tekrar yürütülmeden önce geçmesi gereken minimum süre (saniye cinsinden). 

- **Delay Between Commands (Komutlar Arası Gecikme):** `bluetoothctl` yardımcı programına ardışık komutlar gönderilmesi arasındaki çok kısa bir gecikme (saniye cinsinden). Bazı sistemlerde, küçük bir duraklama eklemek güvenilirliği artırabilir.

- **Process Spawn Timeout (İşlem Başlatma Zaman Aşımı):** `bluetoothctl` sürecinin başlaması için beklenecek maksimum süre (saniye cinsinden). Bu süre içinde başlamazsa, açma girişimi başarısız olur.

- **Pairing Timeout (Eşleştirme Zaman Aşımı):** Basitleştirilmiş açma mantığında, `pair` komutu gönderildikten sonra başarının varsayılması için beklenecek süre miktarıdır. Cihaza uyandırma sinyalini işlemesi için zaman tanır.

- **Bluetooth Scan Duration (Bluetooth Tarama Süresi):** Entegrasyonun eşleştirme komutunu göndermeye çalışmadan önce Bluetooth cihazlarını tarayacağı süre (saniye cinsinden). Daha uzun bir tarama, varlığını yavaşça duyuran cihazları bulmaya yardımcı olabilir.

## Kendi dilinizde okuyun

*   [Afrikaans](README.af.md)
*   [العربية (Arabic)](README.ar.md)
*   [български (Bulgarian)](README.bg.md)
*   [বাংলা (Bengali)](README.bn.md)
*   [Català (Catalan)](README.ca.md)
*   [Čeština (Czech)](README.cs.md)
*   [Dansk (Danish)](README.da.md)
*   [Deutsch (German)](README.de.md)
*   [Deutsch (Schweiz) (German, Switzerland)](README.de-CH.md)
*   [Ελληνικά (Greek)](README.el.md)
*   [English](../README.md)
*   [Español (Spanish)](README.es.md)
*   [Eesti (Estonian)](README.et.md)
*   [Euskara (Basque)](README.eu.md)
*   [فارسی (Persian)](README.fa.md)
*   [Suomi (Finnish)](README.fi.md)
*   [Français (French)](README.fr.md)
*   [Gaeilge (Irish)](README.ga.md)
*   [Galego (Galician)](README.gl.md)
*   [ગુજરાતી (Gujarati)](README.gu.md)
*   [עברית (Hebrew)](README.he.md)
*   [हिन्दी (Hindi)](README.hi.md)
*   [Hrvatski (Croatian)](README.hr.md)
*   [Magyar (Hungarian)](README.hu.md)
*   [Bahasa Indonesia (Indonesian)](README.id.md)
*   [Íslenska (Icelandic)](README.is.md)
*   [Italiano (Italian)](README.it.md)
*   [日本語 (Japanese)](README.ja.md)
*   [ქართული (Georgian)](README.ka.md)
*   [ಕನ್ನಡ (Kannada)](README.kn.md)
*   [한국어 (Korean)](README.ko.md)
*   [Kernewek (Cornish)](README.kw.md)
*   [Lëtzebuergesch (Luxembourgish)](README.lb.md)
*   [Lietuvių (Lithuanian)](README.lt.md)
*   [Latviešu (Latvian)](README.lv.md)
*   [മലയാളം (Malayalam)](README.ml.md)
*   [Монгол (Mongolian)](README.mn.md)
*   [मराठी (Marathi)](README.mr.md)
*   [Bahasa Melayu (Malay)](README.ms.md)
*   [Norsk bokmål (Norwegian Bokmål)](README.nb.md)
*   [नेपाली (Nepali)](README.ne.md)
*   [Nederlands (Dutch)](README.nl.md)
*   [Polski (Polish)](README.pl.md)
*   [Português (Portuguese)](README.pt.md)
*   [Português (Brasil) (Portuguese, Brazil)](README.pt-BR.md)
*   [Română (Romanian)](README.ro.md)
*   [Русский (Russian)](README.ru.md)
*   [Slovenčina (Slovak)](README.sk.md)
*   [Slovenščina (Slovenian)](README.sl.md)
*   [Српски (Serbian)](README.sr.md)
*   [Srpski (latinica) (Serbian, Latin)](README.sr-Latn.md)
*   [Svenska (Swedish)](README.sv.md)
*   [Kiswahili (Swahili)](README.sw.md)
*   [తెలుగు (Telugu)](README.te.md)
*   [ไทย (Thai)](README.th.md)
*   [Türkçe (Turkish)](README.tr.md)
*   [Українська (Ukrainian)](README.uk.md)
*   [اردو (Urdu)](README.ur.md)
*   [Tiếng Việt (Vietnamese)](README.vi.md)
*   [简体中文 (Simplified Chinese)](README.zh-CN.md)
*   [繁體中文 (香港) (Traditional Chinese, Hong Kong)](README.zh-HK.md)

---