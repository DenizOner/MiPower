# MiPower — ہوم اسسٹنٹ کسٹم انٹیگریشن

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** ایک ہوم اسسٹنٹ انٹیگریشن ہے جو آپ کو ایسے میڈیا پلیئرز کی پاور حالت کو کنٹرول کرنے کی اجازت دیتا ہے جو روایتی Wake-on-LAN (WOL) کو سپورٹ نہیں کرتے، لیکن بلوٹوتھ پیئرنگ کی درخواست کے ذریعے "جگائے" جا سکتے ہیں۔ اسے خاص طور پر Xiaomi Mi Box جیسے آلات کے لیے ڈیزائن کیا گیا تھا، لیکن یہ دیگر اسی طرح کے Android TV بکس کے ساتھ بھی کام کر سکتا ہے۔

یہ انٹیگریشن ہوم اسسٹنٹ میں ایک `switch` (سوئچ) اینٹیٹی بناتا ہے۔ 
- سوئچ کو **آن** کرنے سے ڈیوائس کو جگانے کے لیے `bluetoothctl` کے ذریعے بلوٹوتھ کمانڈز کا ایک سلسلہ بھیجا جاتا ہے۔
- سوئچ کو **آف** کرنے سے منسلک ڈیوائس کے لیے `media_player.turn_off` سروس کو کال کیا جاتا ہے۔
- سوئچ کی حالت خود بخود منسلک میڈیا پلیئر اینٹیٹی کی حالت کے ساتھ مطابقت پذیر ہو جاتی ہے۔

## 🤝 تعاون کریں

MiPower پروجیکٹ کو اوپن سورس کمیونٹی میں قدر شامل کرنے کے وژن کے ساتھ تیار کیا جا رہا ہے۔ اس پروجیکٹ کی تسلسل اور ترقی کی رفتار کو برقرار رکھنے کے لیے آپ کی حمایت بہت اہم ہے۔

اگر آپ میری کوششوں کو سراہتے ہیں، تو آپ GitHub Sponsors یا درج ذیل پلیٹ فارمز کے ذریعے میری حمایت کر سکتے ہیں۔ پیشگی شکریہ!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

متبادل کے طور پر، آپ ریپوزٹری کے اوپری دائیں کونے میں **اسپانسر بٹن (❤️)** پر کلک کرکے تمام فنڈنگ کے اختیارات دیکھ سکتے ہیں۔

## پیشگی شرائط

- **Home Assistant OS / Supervised / Container:** اس انٹیگریشن کے لیے ایک Linux-بیسڈ ہوم اسسٹنٹ انسٹالیشن کی ضرورت ہے جہاں `bluetoothctl` کمانڈ لائن یوٹیلیٹی دستیاب اور قابل رسائی ہو۔ یہ ونڈوز پر ہوم اسسٹنٹ کور انسٹالیشن پر **کام نہیں کرے گا**۔

## HACS کے ذریعے انسٹالیشن (تجویز کردہ)

یہ انٹیگریشن HACS میں ایک کسٹم ریپوزٹری کے طور پر دستیاب ہے۔

1.  اپنے HACS ڈیش بورڈ پر جائیں۔
2.  **Integrations** (انٹیگریشنز) پر کلک کریں۔
3.  اوپر دائیں کونے میں تین نقطوں والے مینو پر کلک کریں اور **"Custom repositories"** ("کسٹم ریپوزٹریز") کو منتخب کریں۔
4.  ڈائیلاگ باکس میں، درج ذیل معلومات درج کریں:
    - **Repository (ریپوزٹری):** `https://github.com/DenizOner/MiPower`
    - **Category (کیٹیگری):** `Integration` (انٹیگریشن)
5.  **"Add"** ("شامل کریں") پر کلک کریں۔
6.  "MiPower" انٹیگریشن اب آپ کی HACS فہرست میں ظاہر ہوگی۔ اس پر کلک کریں۔
7.  **"Download"** ("ڈاؤن لوڈ") بٹن پر کلک کریں، اور پھر اگلی ونڈو میں دوبارہ **"Download"** ("ڈاؤن لوڈ") پر کلک کریں۔
8.  ڈاؤن لوڈ مکمل ہونے کے بعد، انٹیگریشن کو لوڈ کرنے کے لیے **آپ کو لازمی طور پر ہوم اسسٹنٹ کو ری اسٹارٹ کرنا چاہیے**۔

## دستی تنصیب

اگرچہ HACS تجویز کردہ طریقہ ہے، آپ انٹیگریشن کو دستی طور پر بھی انسٹال کر سکتے ہیں۔

1.  ریپوزٹری کے [Releases page (ریلیزز صفحہ)](https://github.com/DenizOner/MiPower/releases) پر جائیں اور تازہ ترین ریلیز سے `mipower.zip` فائل ڈاؤن لوڈ کریں۔
2.  ڈاؤن لوڈ کی گئی فائل کو اَن زِپ کریں۔
3.  اَن زِپ شدہ فولڈر کے اندر، آپ کو ایک `custom_components` ڈائرکٹری ملے گی۔ اس کے اندر سے `mipower` فولڈر کو کاپی کریں۔
4.  کاپی شدہ `mipower` فولڈر کو اپنی ہوم اسسٹنٹ کنفیگریشن ڈائرکٹری میں موجود `custom_components` فولڈر میں پیسٹ کریں۔ اگر `custom_components` فولڈر موجود نہیں ہے، تو آپ کو اسے بنانے کی ضرورت ہے۔
    - حتمی راستہ کچھ یوں نظر آنا چاہیے: `.../config/custom_components/mipower/`
5.  ہوم اسسٹنٹ کو ری اسٹارٹ کریں۔

## کنفیگریشن (ترتیب)

ری اسٹارٹ کے بعد، آپ MiPower سوئچ کو شامل اور کنفیگر کر سکتے ہیں۔

1.  **Settings > Devices & Services** (سیٹنگز > ڈیوائسز اور سروسز) پر جائیں۔
2.  نیچے دائیں کونے میں **"+ Add Integration"** ("+ انٹیگریشن شامل کریں") بٹن پر کلک کریں۔
3.  **"MiPower"** تلاش کریں اور اس پر کلک کریں۔

### آسان سیٹ اپ (تجویز کردہ)

یہ انٹیگریشن کو کنفیگر کرنے کا سب سے آسان طریقہ ہے۔

1.  اشارہ کیے جانے پر، **"Easy Setup"** ("آسان سیٹ اپ") کو منتخب کریں۔
2.  انٹیگریشن خود بخود آپ کے سسٹم پر بلوٹوتھ سے فعال میڈیا پلیئرز کو دریافت کرے گی۔
3.  ڈراپ ڈاؤن فہرست سے اپنی ہدف ڈیوائس (مثلاً، "Xiaomi Mi Box 4") کو منتخب کریں۔
4.  **"Submit"** ("جمع کرائیں") پر کلک کریں۔

بس! انٹیگریشن آپ کے میڈیا پلیئر سے منسلک ایک سوئچ بنائے گا۔

### ایڈوانسڈ سیٹ اپ

اگر آسان سیٹ اپ آپ کی ڈیوائس کو نہیں ڈھونڈتا ہے یا اگر آپ کو شروع سے ہی ایڈوانسڈ ٹائمنگ سیٹنگز کو کنفیگر کرنے کی ضرورت ہے تو یہ طریقہ استعمال کریں۔

1.  **مرحلہ 1: ڈیوائس کا انتخاب**
    - **"Advanced Setup"** ("ایڈوانسڈ سیٹ اپ") کو منتخب کریں۔
    - اپنی ہوم اسسٹنٹ میں موجود *تمام* میڈیا پلیئرز کی فہرست سے اپنے ہدف میڈیا پلیئر کو منتخب کریں۔
2.  **مرحلہ 2: MAC ایڈریس**
    - انٹیگریشن منتخب کردہ ڈیوائس کا بلوٹوتھ MAC ایڈریس تلاش کرنے کی کوشش کرے گا۔ 
    - اگر مل جاتا ہے، تو یہ پہلے سے پُر ہو جائے گا۔ تصدیق کریں کہ یہ درست ہے۔
    - اگر نہیں ملتا ہے، تو آپ کو اپنی ڈیوائس کا بلوٹوتھ MAC ایڈریس دستی طور پر درج کرنا ہوگا۔
3.  **مرحلہ 3: ٹائمنگ سیٹنگز**
    - آپ بلوٹوتھ کمانڈز کے لیے مختلف ٹائم آؤٹ اور تاخیر کو کنفیگر کر سکتے ہیں۔ زیادہ تر صارفین کے لیے، ڈیفالٹ ویلیوز کافی ہیں۔
4.  سیٹ اپ مکمل کرنے کے لیے **"Submit"** ("جمع کرائیں") پر کلک کریں۔

## آپشنز (اختیارات)

اپنے MiPower سوئچ کو کنفیگر کرنے کے بعد، آپ کسی بھی وقت ٹائمنگ سیٹنگز کو ایڈجسٹ کر سکتے ہیں۔

1.  **Settings > Devices & Services** (سیٹنگز > ڈیوائسز اور سروسز) پر جائیں۔
2.  MiPower انٹیگریشن تلاش کریں اور **"Configure"** ("کنفیگر کریں") پر کلک کریں۔
3.  ضرورت کے مطابق *debounce*، ٹائم آؤٹس، اور تاخیر کے سلائیڈرز کو ایڈجسٹ کریں۔

## ٹائمنگ سیٹنگز کی وضاحت

کنفیگریشن یا آپشنز مینو میں، آپ بلوٹوتھ کمانڈز کی ٹائمنگ کو ٹھیک ٹ्यून کر سکتے ہیں۔ زیادہ تر صارفین کے لیے، ڈیفالٹ ویلیوز اچھی طرح سے کام کرتی ہیں۔

- **Turn-On Debounce (آن کرنے کا ڈیباؤنس):** کم سے کم وقت (سیکنڈ میں) جو 'آن کریں' کمانڈ کے دوبارہ چلائے جانے سے پہلے گزرنا چاہیے۔ اگر سوئچ کو تیزی سے ٹوگل کیا جاتا ہے تو یہ ڈیوائس کو ویک-اَپ سگنلز کے ساتھ سپیم ہونے سے روکتا ہے۔

- **Turn-Off Debounce (آف کرنے کا ڈیباؤنس):** کم سے کم وقت (سیکنڈ میں) جو 'آف کریں' کمانڈ کے دوبارہ چلائے جانے سے پہلے گزرنا چاہیے۔ 

- **Delay Between Commands (کمانڈز کے درمیان تاخیر):** `bluetoothctl` یوٹیلیٹی کو مسلسل کمانڈز بھیجنے کے درمیان ایک بہت ہی مختصر تاخیر (سیکنڈ میں)۔ کچھ سسٹمز پر، ایک چھوٹا سا وقفہ شامل کرنے سے وشوسنییتا بہتر ہو سکتی ہے۔

- **Process Spawn Timeout (پروسیس شروع ہونے کا ٹائم آؤٹ):** `bluetoothctl` پروسیس کے شروع ہونے کا انتظار کرنے کا زیادہ سے زیادہ وقت (سیکنڈ میں)۔ اگر یہ اس وقت کے اندر شروع ہونے میں ناکام ہو جاتا ہے، تو آن کرنے کی کوشش ناکام ہو جائے گی۔

- **Pairing Timeout (پیئرنگ کا ٹائم آؤٹ):** آسان کردہ آن لاجک میں، یہ وہ وقت ہے جو کامیابی فرض کرنے سے پہلے `pair` کمانڈ بھیجنے کے بعد انتظار کرنا ہے۔ یہ ڈیوائس کو ویک-اَپ سگنل پر عمل کرنے کا وقت دیتا ہے۔

- **Bluetooth Scan Duration (بلوٹوتھ اسکین کا دورانیہ):** وہ دورانیہ (سیکنڈ میں) جو انٹیگریشن پیئر کمانڈ بھیجنے کی کوشش کرنے سے پہلے بلوٹوتھ ڈیوائسز کے لیے اسکین کرے گا۔ ایک طویل اسکین ان ڈیوائسز کو تلاش کرنے میں مدد کر سکتا ہے جو اپنی موجودگی کا اشتہار دینے میں سست ہیں۔

## اپنی زبان میں پڑھیں

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