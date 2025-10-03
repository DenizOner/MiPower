# MiPower — Home Assistant-ийн өөрчлөн тохируулсан интеграц

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** нь уламжлалт Wake-on-LAN (WOL)-г дэмждэггүй боловч Bluetooth-ийн хослол (pairing) хүсэлтээр "сэрээгдэх" боломжтой медиа тоглуулагчийн цахилгаан хангамжийн төлөвийг удирдах боломжийг олгодог Home Assistant-ийн интеграц юм. Энэ нь Xiaomi Mi Box зэрэг төхөөрөмжүүдэд зориулагдан бүтээгдсэн боловч бусад ижил төстэй Android TV хайрцагт ажиллах боломжтой.

Энэхүү интеграц нь Home Assistant-д `switch` (товчлуур) энтити үүсгэдэг. 
- Товчлуурыг **АСААХ** нь төхөөрөмжийг сэрээхийн тулд `bluetoothctl`-ээр дамжуулан Bluetooth командуудын цувралыг илгээдэг.
- Товчлуурыг **УНТРААХ** нь холбогдсон төхөөрөмжийн `media_player.turn_off` үйлчилгээг дууддаг.
- Товчлуурын төлөв нь холбогдсон медиа тоглуулагчийн энтитийн төлөвтэй автоматаар синхрончлогддог.

## 🤝 Дэмжлэг үзүүлэх

MiPower төсөл нь нээлттэй эхийн хамт олонд үнэ цэнэ нэмэх алсын хараатайгаар хөгжүүлэгдэж байна. Энэ төслийн тасралтгүй байдал, хөгжлийн хурдыг хадгалахад таны дэмжлэг чухал ач холбогдолтой.

Хэрэв та миний хөдөлмөрийг үнэлж байвал GitHub ивээн тэтгэгч эсвэл доорх платформуудаар дамжуулан намайг дэмжиж болно. Урьдчилж баярлалаа!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Өөрөөр хэлбэл, та репозиторын баруун дээд буланд байрлах **Ивээн тэтгэгч товчлуур (❤️)** дээр дарж санхүүжилтийн бүх сонголтыг харах боломжтой.

## Урьдчилсан нөхцөл

- **Home Assistant OS / Supervised / Container:** Энэхүү интеграц нь `bluetoothctl` командын мөрийн хэрэгсэл бэлэн бөгөөд нэвтрэх боломжтой Linux дээр суурилсан Home Assistant-ийн суурилуулалтыг шаарддаг. Энэ нь Windows дээрх Home Assistant Core-ийн суурилуулалтад **ажиллахгүй**.

## HACS-ээр дамжуулан суулгах (Зөвлөмж)

Энэхүү интеграц нь HACS-д өөрчлөн тохируулсан репозитори хэлбэрээр байдаг.

1.  Өөрийн HACS хяналтын самбар руу очно уу.
2.  **Integrations** (Интеграцууд)-г дарна уу.
3.  Баруун дээд буланд байрлах гурван цэг бүхий цэсийг дарж **"Custom repositories"** ("Өөрчлөн тохируулсан репозиторууд")-г сонгоно уу.
4.  Харилцах цонхонд дараах мэдээллийг оруулна уу:
    - **Repository (Репозитори):** `https://github.com/DenizOner/MiPower`
    - **Category (Ангилал):** `Integration` (Интеграц)
5.  **"Add"** ("Нэмэх")-г дарна уу.
6.  "MiPower" интеграц одоо таны HACS жагсаалтад гарч ирнэ. Үүнийг дарна уу.
7.  **"Download"** ("Татах") товчийг дарж, дараа нь гарч ирэх цонхонд дахин **"Download"** ("Татах")-г дарна уу.
8.  Татан авалт дууссаны дараа интеграцийг ачаалахын тулд **Home Assistant-г дахин эхлүүлэх шаардлагатай**.

## Гараар суулгах

HACS нь зөвлөмж болгосон арга боловч та интеграцийг гараар суулгаж болно.

1.  Репозиторийн [Release Page](https://github.com/DenizOner/MiPower/releases) руу орж, хамгийн сүүлийн хувилбараас `mipower.zip` файлыг татаж авна уу.
2.  Татаж авсан файлыг задлаад (unzip) гаргана уу.
3.  Задлагдсан хавтас дотор та `custom_components` директорийг олох болно. Түүнээс `mipower` хавтасыг хуулж авна уу.
4.  Хуулсан `mipower` хавтасыг Home Assistant-ийн тохиргооны директорийг `custom_components` хавтас руу буулгана уу. Хэрэв `custom_components` хавтас байхгүй бол та үүнийг үүсгэх хэрэгтэй.
    - Эцсийн зам нь дараахтай төстэй байх ёстой: `.../config/custom_components/mipower/`
5.  Home Assistant-г дахин эхлүүлнэ үү.

## Тохиргоо

Дахин эхлүүлсний дараа та MiPower товчлуурыг нэмж, тохируулж болно.

1.  **Settings > Devices & Services** (Тохиргоо > Төхөөрөмж ба Үйлчилгээнүүд) руу очно уу.
2.  Баруун доод буланд байрлах **"+ Add Integration"** ("+ Интеграц нэмэх") товчийг дарна уу.
3.  **"MiPower"**-г хайж, дарна уу.

### Хялбар тохиргоо (Зөвлөмж)

Энэ нь интеграцийг тохируулах хамгийн энгийн арга юм.

1.  Асуухад, **"Easy Setup"** ("Хялбар тохиргоо")-г сонгоно уу.
2.  Интеграц нь таны систем дээрх Bluetooth-тэй медиа тоглуулагчийг автоматаар илрүүлдэг.
3.  Унжуулах жагсаалтаас өөрийн зорилтот төхөөрөмжийг (жишээлбэл, "Xiaomi Mi Box 4") сонгоно уу.
4.  **"Submit"** ("Илгээх")-г дарна уу.

Ингээд л боллоо! Интеграц нь таны медиа тоглуулагчтай холбогдсон товчлуурыг үүсгэнэ.

### Нарийвчилсан тохиргоо

Хэрэв Хялбар тохиргоо таны төхөөрөмжийг олохгүй байвал эсвэл эхнээс нь нарийвчилсан цаг хугацааны тохиргоог хийх шаардлагатай бол энэ аргыг ашиглана уу.

1.  **Алхам 1: Төхөөрөмж сонгох**
    - **"Advanced Setup"** ("Нарийвчилсан тохиргоо")-г сонгоно уу.
    - Өөрийн Home Assistant дээрх *бүх* медиа тоглуулагчийн жагсаалтаас зорилтот медиа тоглуулагчаа сонгоно уу.
2.  **Алхам 2: MAC хаяг**
    - Интеграц нь сонгосон төхөөрөмжийн Bluetooth MAC хаягийг олохыг оролдоно. 
    - Хэрэв олдвол, урьдчилан бөглөгдөнө. Үүнийг зөв эсэхийг шалгана уу.
    - Олдохгүй бол та өөрийн төхөөрөмжийн Bluetooth MAC хаягийг гараар оруулах шаардлагатай.
3.  **Алхам 3: Цаг хугацааны тохиргоо**
    - Та Bluetooth командуудын хувьд янз бүрийн хугацаа болон саатал зэргийг тохируулж болно. Ихэнх хэрэглэгчдийн хувьд анхдагч утгууд хангалттай.
4.  Тохиргоог дуусгахын тулд **"Submit"** ("Илгээх")-г дарна уу.

## Сонголтууд

Та MiPower товчлуураа тохируулсны дараа хүссэн үедээ цаг хугацааны тохиргоог тохируулж болно.

1.  **Settings > Devices & Services** (Тохиргоо > Төхөөрөмж ба Үйлчилгээнүүд) руу очно уу.
2.  MiPower интеграцийг олж, **"Configure"** ("Тохируулах")-г дарна уу.
3.  Шаардлагатай бол *debounce*, хугацаа болон саатлын гулсагчийг тохируулна уу.

## Цаг хугацааны тохиргооны тайлбар

Тохиргоо эсвэл сонголтын цэсэнд та Bluetooth командуудын цаг хугацааг нарийн тохируулж болно. Ихэнх хэрэглэгчдийн хувьд анхдагч утгууд сайн ажилладаг.

- **Turn-On Debounce (Асаах саатал):** 'Асаах' командыг дахин гүйцэтгэхээс өмнө өнгөрөх ёстой хамгийн бага хугацаа (секундээр). Энэ нь товчлуурыг хурдан товшлоход төхөөрөмжийг сэрээх дохиогоор спамдахаас сэргийлдэг.

- **Turn-Off Debounce (Унтраах саатал):** 'Унтраах' командыг дахин гүйцэтгэхээс өмнө өнгөрөх ёстой хамгийн бага хугацаа (секундээр). 

- **Delay Between Commands (Командуудын хоорондох саатал):** `bluetoothctl` хэрэгсэлд дараалсан командуудыг илгээх хоорондох маш богино саатал (секундээр). Зарим систем дээр бага зэрэг түр зогсолт нэмэх нь найдвартай байдлыг сайжруулдаг.

- **Process Spawn Timeout (Процесс эхлүүлэх хугацаа):** `bluetoothctl` процесс эхлэхийг хүлээх дээд хугацаа (секундээр). Хэрэв энэ хугацаанд эхлэхгүй бол асаах оролдлого амжилтгүй болно.

- **Pairing Timeout (Хослолын хугацаа):** Хялбаршуулсан асаах логикт, энэ нь `pair` командыг илгээсний дараа амжилттай болсон гэж үзэхээс өмнө хүлээх хугацаа юм. Энэ нь төхөөрөмжид сэрээх дохиог боловсруулах цаг өгдөг.

- **Bluetooth Scan Duration (Bluetooth скан хийх хугацаа):** Хослолын командыг илгээхийг оролдохоос өмнө интеграц нь Bluetooth төхөөрөмжүүдийг скан хийх хугацаа (секундээр). Илүү урт скан хийх нь өөрсдийн оршин тогтнолыг удаан зарладаг төхөөрөмжүүдийг олоход тусална.

## Өөрийн хэлээр унших

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