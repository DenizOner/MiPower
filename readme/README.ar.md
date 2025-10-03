# MiPower - تكامل مخصص لـ Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** هو تكامل لـ Home Assistant يسمح لك بالتحكم في حالة الطاقة لمشغلات الوسائط التي لا تدعم خاصية Wake-on-LAN (WOL) التقليدية ولكن يمكن "إيقاظها" عن طريق طلب اقتران Bluetooth. لقد تم تصميمه خصيصًا لأجهزة مثل Xiaomi Mi Box، ولكنه قد يعمل مع صناديق Android TV المماثلة الأخرى.

ينشئ هذا التكامل كيان `switch` (مفتاح) في Home Assistant. 
- **تشغيل** المفتاح يرسل سلسلة من أوامر Bluetooth عبر `bluetoothctl` لإيقاظ الجهاز.
- **إيقاف تشغيل** المفتاح يستدعي خدمة `media_player.turn_off` للجهاز المرتبط.
- تتم مزامنة حالة المفتاح تلقائيًا مع حالة كيان مشغل الوسائط المرتبط.

## 🤝 ادعم المشروع

يتم تطوير مشروع MiPower برؤية تتمثل في إضافة قيمة إلى مجتمع المصادر المفتوحة. دعمكم حيوي للحفاظ على استمرارية المشروع وسرعة تطويره.

إذا كنتم تقدّرون جهدي، يمكنكم دعمي عبر رعاية GitHub Sponsors أو المنصات التالية. شكرًا لكم مقدمًا!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

بدلاً من ذلك، يمكنك رؤية جميع خيارات التمويل بالنقر على **زر الراعي (❤️)** في الزاوية اليمنى العليا من المستودع.

## المتطلبات الأساسية

- **Home Assistant OS / Supervised / Container:** يتطلب هذا التكامل تثبيت Home Assistant قائمًا على نظام Linux حيث تتوفر أداة سطر الأوامر `bluetoothctl` ويسهل الوصول إليها. لن يعمل **على الإطلاق** على تثبيت Home Assistant Core على نظام Windows.

## التثبيت عبر HACS (موصى به)

يتوفر هذا التكامل كمستودع مخصص في HACS.

1.  انتقل إلى لوحة معلومات HACS الخاصة بك.
2.  انقر على **Integrations** (التكاملات).
3.  انقر فوق قائمة النقاط الثلاث في الزاوية العلوية اليمنى وحدد **"Custom repositories"** ("المستودعات المخصصة").
4.  في مربع الحوار، أدخل المعلومات التالية:
    - **Repository (المستودع):** `https://github.com/DenizOner/MiPower`
    - **Category (الفئة):** `Integration` (تكامل)
5.  انقر فوق **"Add"** ("إضافة").
6.  سيظهر تكامل "MiPower" الآن في قائمة HACS الخاصة بك. انقر فوقه.
7.  انقر على زر **"Download"** ("تنزيل") ثم انقر على **"Download"** ("تنزيل") مرة أخرى في النافذة التالية.
8.  بعد اكتمال التنزيل، **يجب عليك إعادة تشغيل Home Assistant** لتحميل التكامل.

## التثبيت اليدوي

على الرغم من أن HACS هي الطريقة الموصى بها، يمكنك أيضًا تثبيت التكامل يدويًا.

1.  اذهب إلى [صفحة الإصدارات](https://github.com/DenizOner/MiPower/releases) للمستودع وقم بتنزيل ملف `mipower.zip` من أحدث إصدار.
2.  قم بفك ضغط الملف الذي تم تنزيله.
3.  داخل المجلد غير المضغوط، ستجد دليل `custom_components`. انسخ مجلد `mipower` من داخله.
4.  الصق مجلد `mipower` المنسوخ في مجلد `custom_components` في دليل تكوين Home Assistant الخاص بك. إذا لم يكن مجلد `custom_components` موجودًا، فأنت بحاجة إلى إنشائه.
    - يجب أن يبدو المسار النهائي كما يلي: `.../config/custom_components/mipower/`
5.  أعد تشغيل Home Assistant.

## التكوين

بعد إعادة التشغيل، يمكنك إضافة مفتاح MiPower وتكوينه.

1.  اذهب إلى **Settings > Devices & Services** (الإعدادات > الأجهزة والخدمات).
2.  انقر على زر **"+ Add Integration"** ("+ إضافة تكامل") في الزاوية السفلية اليمنى.
3.  ابحث عن **"MiPower"** وانقر عليه.

### الإعداد السهل (موصى به)

هذه هي أبسط طريقة لتكوين التكامل.

1.  عند المطالبة، اختر **"Easy Setup"** ("الإعداد السهل").
2.  سيكتشف التكامل تلقائيًا مشغلات الوسائط التي تدعم تقنية Bluetooth على نظامك.
3.  حدد جهازك الهدف (مثل "Xiaomi Mi Box 4") من القائمة المنسدلة.
4.  انقر فوق **"Submit"** ("إرسال").

هذا كل شيء! سيقوم التكامل بإنشاء مفتاح مرتبط بمشغل الوسائط الخاص بك.

### الإعداد المتقدم

استخدم هذه الطريقة إذا لم يجد الإعداد السهل جهازك أو إذا كنت بحاجة إلى تكوين إعدادات التوقيت المتقدمة منذ البداية.

1.  **الخطوة 1: اختيار الجهاز**
    - اختر **"Advanced Setup"** ("الإعداد المتقدم").
    - حدد مشغل الوسائط الهدف الخاص بك من قائمة *جميع* مشغلات الوسائط في Home Assistant الخاص بك.
2.  **الخطوة 2: عنوان MAC**
    - سيحاول التكامل العثور على عنوان Bluetooth MAC للجهاز المحدد. 
    - إذا تم العثور عليه، فسيتم ملؤه مسبقًا. تحقق من أنه صحيح.
    - إذا لم يتم العثور عليه، يجب عليك إدخال عنوان Bluetooth MAC الخاص بجهازك يدويًا.
3.  **الخطوة 3: إعدادات التوقيت**
    - يمكنك تكوين مهل زمنية وتأخيرات مختلفة لأوامر Bluetooth. بالنسبة لمعظم المستخدمين، فإن القيم الافتراضية كافية.
4.  انقر فوق **"Submit"** ("إرسال") لإكمال الإعداد.

## الخيارات

بعد تكوين مفتاح MiPower الخاص بك، يمكنك ضبط إعدادات التوقيت في أي وقت.

1.  اذهب إلى **Settings > Devices & Services** (الإعدادات > الأجهزة والخدمات).
2.  ابحث عن تكامل MiPower وانقر على **"Configure"** ("تكوين").
3.  اضبط أشرطة التمرير الخاصة بالتخفيف، والمهل الزمنية، والتأخيرات حسب الحاجة.

## شرح إعدادات التوقيت

في قائمة التكوين أو الخيارات، يمكنك ضبط توقيت أوامر Bluetooth بدقة. بالنسبة لمعظم المستخدمين، تعمل القيم الافتراضية جيدًا.

- **Turn-On Debounce (تخفيف التشغيل):** الحد الأدنى للوقت (بالثواني) الذي يجب أن يمر قبل أن يتم تنفيذ أمر 'التشغيل' مرة أخرى. هذا يمنع إغراق الجهاز بإشارات الاستيقاظ إذا تم تبديل المفتاح بسرعة.

- **Turn-Off Debounce (تخفيف إيقاف التشغيل):** الحد الأدنى للوقت (بالثواني) الذي يجب أن يمر قبل أن يتم تنفيذ أمر 'إيقاف التشغيل' مرة أخرى. 

- **Delay Between Commands (التأخير بين الأوامر):** تأخير قصير جدًا (بالثواني) بين إرسال الأوامر المتتالية إلى أداة `bluetoothctl` المساعدة. في بعض الأنظمة، يمكن أن يؤدي إضافة وقفة قصيرة إلى تحسين الموثوقية.

- **Process Spawn Timeout (مهلة بدء العملية):** الحد الأقصى للوقت (بالثواني) للانتظار حتى تبدأ عملية `bluetoothctl`. إذا فشلت في البدء خلال هذا الوقت، فسوف تفشل محاولة التشغيل.

- **Pairing Timeout (مهلة الاقتران):** في منطق التشغيل المبسط، هذه هي مقدار الوقت الذي يجب انتظاره بعد إرسال أمر `pair` قبل افتراض النجاح. يمنح الجهاز وقتًا لمعالجة إشارة الاستيقاظ.

- **Bluetooth Scan Duration (مدة مسح البلوتوث):** المدة (بالثواني) التي سيقوم خلالها التكامل بالبحث عن أجهزة Bluetooth قبل محاولة إرسال أمر الاقتران. يمكن أن يساعد الفحص الأطول في العثور على الأجهزة البطيئة في الإعلان عن وجودها.

## اقرأ بلغتك الخاصة

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