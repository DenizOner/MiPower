# MiPower — ادغام سفارشی Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** یک ادغام Home Assistant است که به شما اجازه می‌دهد تا وضعیت برق پخش‌کننده‌های رسانه‌ای را کنترل کنید که از Wake-on-LAN (WOL) سنتی پشتیبانی نمی‌کنند، اما می‌توانند توسط یک درخواست جفت‌سازی بلوتوث "بیدار" شوند. این برنامه به طور خاص برای دستگاه‌هایی مانند Xiaomi Mi Box طراحی شده بود، اما ممکن است با دیگر جعبه‌های Android TV مشابه نیز کار کند.

این ادغام یک موجودیت `switch` (سوئیچ) در Home Assistant ایجاد می‌کند. 
- **روشن کردن** سوئیچ، یک سری از دستورات بلوتوث را از طریق `bluetoothctl` برای بیدار کردن دستگاه ارسال می‌کند.
- **خاموش کردن** سوئیچ، سرویس `media_player.turn_off` را برای دستگاه مرتبط فراخوانی می‌کند.
- وضعیت سوئیچ به طور خودکار با وضعیت موجودیت پخش‌کننده رسانه‌ای مرتبط، همگام‌سازی می‌شود.

## 🤝 از ما حمایت کنید

پروژه MiPower با چشم‌انداز افزودن ارزش به جامعه منبع باز در حال توسعه است. حمایت شما برای حفظ تداوم و سرعت توسعه این پروژه حیاتی است.

اگر کار من را ارج می‌نهید، می‌توانید از طریق GitHub Sponsors یا پلتفرم‌های زیر از من حمایت کنید. پیشاپیش سپاسگزارم!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

به عنوان جایگزین، می‌توانید با کلیک بر روی **دکمه حامی (❤️)** در گوشه سمت راست بالای مخزن، تمام گزینه‌های تأمین مالی را مشاهده کنید.

## پیش‌نیازها

- **Home Assistant OS / Supervised / Container:** این ادغام به یک نصب Home Assistant مبتنی بر لینوکس نیاز دارد که در آن ابزار خط فرمان `bluetoothctl` در دسترس و قابل دسترسی باشد. این برنامه **در نصب Home Assistant Core روی ویندوز کار نخواهد کرد.**

## نصب از طریق HACS (توصیه شده)

این ادغام به عنوان یک مخزن سفارشی در HACS در دسترس است.

1.  به داشبورد HACS خود بروید.
2.  روی **Integrations** (ادغام‌ها) کلیک کنید.
3.  روی منوی سه نقطه در گوشه بالا سمت راست کلیک کرده و **"Custom repositories"** ("مخازن سفارشی") را انتخاب کنید.
4.  در کادر محاوره‌ای، اطلاعات زیر را وارد کنید:
    - **Repository (مخزن):** `https://github.com/DenizOner/MiPower`
    - **Category (دسته):** `Integration` (ادغام)
5.  روی **"Add"** ("افزودن") کلیک کنید.
6.  ادغام "MiPower" اکنون در لیست HACS شما ظاهر می‌شود. روی آن کلیک کنید.
7.  روی دکمه **"Download"** ("دانلود") کلیک کنید و سپس دوباره در پنجره بعدی روی **"Download"** ("دانلود") کلیک کنید.
8.  پس از اتمام دانلود، **باید Home Assistant را مجدداً راه‌اندازی کنید** تا ادغام بارگیری شود.

## نصب دستی

اگرچه HACS روش توصیه شده است، می‌توانید ادغام را به صورت دستی نیز نصب کنید.

1.  به [صفحه نسخه‌ها](https://github.com/DenizOner/MiPower/releases) مخزن بروید و فایل `mipower.zip` را از آخرین نسخه دانلود کنید.
2.  فایل دانلود شده را از حالت فشرده خارج کنید.
3.  در داخل پوشه خارج شده از حالت فشرده، یک دایرکتوری `custom_components` پیدا خواهید کرد. پوشه `mipower` را از داخل آن کپی کنید.
4.  پوشه کپی شده `mipower` را در پوشه `custom_components` در دایرکتوری پیکربندی Home Assistant خود جای‌گذاری (Paste) کنید. اگر پوشه `custom_components` وجود ندارد، باید آن را ایجاد کنید.
    - مسیر نهایی باید به این صورت باشد: `.../config/custom_components/mipower/`
5.  Home Assistant را مجدداً راه‌اندازی کنید.

## پیکربندی

پس از راه‌اندازی مجدد، می‌توانید سوئیچ MiPower را اضافه و پیکربندی کنید.

1.  به **Settings > Devices & Services** (تنظیمات > دستگاه‌ها و خدمات) بروید.
2.  روی دکمه **"+ Add Integration"** ("+ افزودن ادغام") در گوشه پایین سمت راست کلیک کنید.
3.  **"MiPower"** را جستجو کرده و روی آن کلیک کنید.

### تنظیم آسان (توصیه شده)

این ساده‌ترین راه برای پیکربندی ادغام است.

1.  هنگام درخواست، **"Easy Setup"** ("تنظیم آسان") را انتخاب کنید.
2.  ادغام به طور خودکار پخش‌کننده‌های رسانه‌ای دارای بلوتوث را در سیستم شما کشف خواهد کرد.
3.  دستگاه مورد نظر خود (به عنوان مثال، "Xiaomi Mi Box 4") را از لیست کشویی انتخاب کنید.
4.  روی **"Submit"** ("ارسال") کلیک کنید.

همین است! این ادغام یک سوئیچ مرتبط با پخش‌کننده رسانه‌ای شما ایجاد خواهد کرد.

### تنظیمات پیشرفته

اگر تنظیم آسان دستگاه شما را پیدا نکرد یا اگر نیاز به پیکربندی تنظیمات زمان‌بندی پیشرفته از ابتدا دارید، از این روش استفاده کنید.

1.  **مرحله 1: انتخاب دستگاه**
    - **"Advanced Setup"** ("تنظیمات پیشرفته") را انتخاب کنید.
    - پخش‌کننده رسانه‌ای مورد نظر خود را از لیست *همه* پخش‌کننده‌های رسانه‌ای در Home Assistant خود انتخاب کنید.
2.  **مرحله 2: آدرس MAC**
    - ادغام سعی خواهد کرد آدرس Bluetooth MAC دستگاه انتخاب شده را پیدا کند. 
    - در صورت پیدا شدن، از قبل پر خواهد شد. صحت آن را تأیید کنید.
    - در صورت عدم پیدا شدن، باید آدرس Bluetooth MAC دستگاه خود را به صورت دستی وارد کنید.
3.  **مرحله 3: تنظیمات زمان‌بندی**
    - می‌توانید زمان‌بندی‌ها و تأخیرهای مختلفی را برای دستورات بلوتوث پیکربندی کنید. برای اکثر کاربران، مقادیر پیش‌فرض کافی هستند.
4.  برای تکمیل تنظیم، روی **"Submit"** ("ارسال") کلیک کنید.

## گزینه‌ها

هنگامی که سوئیچ MiPower خود را پیکربندی کردید، می‌توانید تنظیمات زمان‌بندی را در هر زمان تنظیم کنید.

1.  به **Settings > Devices & Services** (تنظیمات > دستگاه‌ها و خدمات) بروید.
2.  ادغام MiPower را پیدا کرده و روی **"Configure"** ("پیکربندی") کلیک کنید.
3.  لغزنده‌های مربوط به *debounce*، زمان‌بندی‌ها و تأخیرها را در صورت نیاز تنظیم کنید.

## توضیح تنظیمات زمان‌بندی

در منوی پیکربندی یا گزینه‌ها، می‌توانید زمان‌بندی دستورات بلوتوث را به دقت تنظیم کنید. برای اکثر کاربران، مقادیر پیش‌فرض به خوبی کار می‌کنند.

- **Turn-On Debounce (خنثی‌سازی لرزش روشن شدن):** حداقل زمانی (بر حسب ثانیه) که باید بگذرد تا دستور 'روشن کردن' بتواند دوباره اجرا شود. این کار از ارسال سیگنال‌های بیدارباش زیاد به دستگاه در صورت سریع خاموش و روشن شدن سوئیچ جلوگیری می‌کند.

- **Turn-Off Debounce (خنثی‌سازی لرزش خاموش شدن):** حداقل زمانی (بر حسب ثانیه) که باید بگذرد تا دستور 'خاموش کردن' بتواند دوباره اجرا شود. 

- **Delay Between Commands (تأخیر بین دستورات):** یک تأخیر بسیار کوتاه (بر حسب ثانیه) بین ارسال دستورات متوالی به ابزار `bluetoothctl`. در برخی سیستم‌ها، افزودن یک مکث کوچک می‌تواند قابلیت اطمینان را بهبود بخشد.

- **Process Spawn Timeout (مهلت راه‌اندازی فرآیند):** حداکثر زمان (بر حسب ثانیه) برای انتظار برای شروع فرآیند `bluetoothctl`. اگر نتواند در این زمان شروع شود، تلاش برای روشن شدن شکست خواهد خورد.

- **Pairing Timeout (مهلت جفت‌سازی):** در منطق ساده‌شده روشن شدن، این مقدار زمانی است که باید پس از ارسال دستور `pair` قبل از فرض موفقیت، منتظر بمانید. این به دستگاه زمان می‌دهد تا سیگنال بیدارباش را پردازش کند.

- **Bluetooth Scan Duration (مدت زمان اسکن بلوتوث):** مدت زمان (بر حسب ثانیه) که ادغام قبل از تلاش برای ارسال دستور جفت‌سازی، دستگاه‌های بلوتوث را اسکن خواهد کرد. اسکن طولانی‌تر می‌تواند به یافتن دستگاه‌هایی که در اعلام حضور خود کند هستند، کمک کند.

## به زبان خود بخوانید

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