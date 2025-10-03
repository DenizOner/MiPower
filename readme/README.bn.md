# MiPower — হোম অ্যাসিস্ট্যান্ট কাস্টম ইন্টিগ্রেশন

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** হল একটি হোম অ্যাসিস্ট্যান্ট ইন্টিগ্রেশন যা আপনাকে এমন মিডিয়া প্লেয়ারগুলির শক্তি অবস্থা নিয়ন্ত্রণ করতে দেয় যা ঐতিহ্যবাহী ওয়েক-অন-ল্যান (WOL) সমর্থন করে না কিন্তু একটি ব্লুটুথ পেয়ারিং অনুরোধের মাধ্যমে "জাগিয়ে তোলা" যেতে পারে। এটি বিশেষভাবে Xiaomi Mi Box-এর মতো ডিভাইসগুলির জন্য ডিজাইন করা হয়েছিল, তবে এটি অন্যান্য অনুরূপ Android TV বক্সের সাথে কাজ করতে পারে।

এই ইন্টিগ্রেশন হোম অ্যাসিস্ট্যান্ট-এ একটি `switch` সত্তা তৈরি করে। 
- সুইচটি **চালু করা** ডিভাইসটিকে জাগিয়ে তোলার জন্য `bluetoothctl`-এর মাধ্যমে ব্লুটুথ কমান্ডের একটি সিরিজ পাঠায়।
- সুইচটি **বন্ধ করা** লিঙ্ক করা ডিভাইসটির জন্য `media_player.turn_off` পরিষেবাটিকে কল করে।
- সুইচটির অবস্থা স্বয়ংক্রিয়ভাবে লিঙ্ক করা মিডিয়া প্লেয়ার সত্তার অবস্থার সাথে সিঙ্ক্রোনাইজ করা হয়।

## 🤝 সমর্থন করুন

MiPower প্রকল্পটি ওপেন সোর্স কমিউনিটিতে মান যোগ করার লক্ষ্য নিয়ে তৈরি করা হচ্ছে। এই প্রকল্পের ধারাবাহিকতা এবং উন্নয়নের গতি বজায় রাখার জন্য আপনার সমর্থন অপরিহার্য।

যদি আপনি আমার প্রচেষ্টার প্রশংসা করেন, আপনি GitHub Sponsors বা নিম্নলিখিত প্ল্যাটফর্মগুলির মাধ্যমে আমাকে সমর্থন করতে পারেন। আগাম ধন্যবাদ!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

বিকল্পভাবে, আপনি রিপোজিটরিটির উপরের ডান কোণে **স্পন্সর বাটনে (❤️)** ক্লিক করে সমস্ত অর্থায়নের বিকল্প দেখতে পারেন।

## পূর্বশর্ত

- **Home Assistant OS / Supervised / Container:** এই ইন্টিগ্রেশনটির জন্য একটি লিনাক্স-ভিত্তিক হোম অ্যাসিস্ট্যান্ট ইনস্টলেশন প্রয়োজন যেখানে `bluetoothctl` কমান্ড-লাইন সরঞ্জামটি উপলব্ধ এবং অ্যাক্সেসযোগ্য। এটি উইন্ডোজে একটি হোম অ্যাসিস্ট্যান্ট কোর ইনস্টলেশনে **কাজ করবে না**।

## HACS-এর মাধ্যমে ইনস্টলেশন (প্রস্তাবিত)

এই ইন্টিগ্রেশনটি HACS-এ একটি কাস্টম রিপোজিটরি হিসাবে উপলব্ধ।

1.  আপনার HACS ড্যাশবোর্ডে নেভিগেট করুন।
2.  **Integrations** (ইন্টিগ্রেশনস)-এ ক্লিক করুন।
3.  উপরের ডান কোণে তিনটি বিন্দুর মেনুতে ক্লিক করুন এবং **"Custom repositories"** ("কাস্টম রিপোজিটরি") নির্বাচন করুন।
4.  ডায়ালগ বক্সে, নিম্নলিখিত তথ্য লিখুন:
    - **Repository (রিপোজিটরি):** `https://github.com/DenizOner/MiPower`
    - **Category (ক্যাটাগরি):** `Integration` (ইন্টিগ্রেশন)
5.  **"Add"** ("যোগ করুন") ক্লিক করুন।
6.  "MiPower" ইন্টিগ্রেশনটি এখন আপনার HACS তালিকায় উপস্থিত হবে। এটির উপর ক্লিক করুন।
7.  **"Download"** ("ডাউনলোড") বোতামে ক্লিক করুন এবং তারপর পরবর্তী উইন্ডোতে আবার **"Download"** ("ডাউনলোড") ক্লিক করুন।
8.  ডাউনলোড সম্পূর্ণ হওয়ার পরে, ইন্টিগ্রেশন লোড হওয়ার জন্য আপনাকে **অবশ্যই হোম অ্যাসিস্ট্যান্ট রিস্টার্ট করতে হবে**।

## ম্যানুয়াল ইনস্টলেশন

যদিও HACS হল প্রস্তাবিত পদ্ধতি, আপনি ম্যানুয়ালিও ইন্টিগ্রেশনটি ইনস্টল করতে পারেন।

1.  রিপোজিটরিটির [Releases page](https://github.com/DenizOner/MiPower/releases)-এ যান এবং সর্বশেষ রিলিজ থেকে `mipower.zip` ফাইলটি ডাউনলোড করুন।
2.  ডাউনলোড করা ফাইলটি আনজিপ করুন।
3.  আনজিপ করা ফোল্ডারের ভিতরে, আপনি একটি `custom_components` ডিরেক্টরি পাবেন। এর মধ্যে থেকে `mipower` ফোল্ডারটি কপি করুন।
4.  আপনার হোম অ্যাসিস্ট্যান্ট কনফিগারেশন ডিরেক্টরিতে `custom_components` ফোল্ডারের মধ্যে কপি করা `mipower` ফোল্ডারটি পেস্ট করুন। যদি `custom_components` ফোল্ডারটি বিদ্যমান না থাকে, তবে আপনাকে এটি তৈরি করতে হবে।
    - চূড়ান্ত পথটি এমন হওয়া উচিত: `.../config/custom_components/mipower/`
5.  হোম অ্যাসিস্ট্যান্ট রিস্টার্ট করুন।

## কনফিগারেশন

রিস্টার্ট করার পরে, আপনি MiPower সুইচটি যোগ এবং কনফিগার করতে পারেন।

1.  **Settings > Devices & Services** (সেটিংস > ডিভাইস এবং পরিষেবা) এ যান।
2.  নীচের ডান কোণে **"+ Add Integration"** ("+ ইন্টিগ্রেশন যোগ করুন") বোতামে ক্লিক করুন।
3.  **"MiPower"** অনুসন্ধান করুন এবং এটির উপর ক্লিক করুন।

### সহজ সেটআপ (প্রস্তাবিত)

ইন্টিগ্রেশন কনফিগার করার এটি হল সবচেয়ে সহজ উপায়।

1.  যখন প্রম্পট করা হবে, **"Easy Setup"** ("সহজ সেটআপ") বেছে নিন।
2.  ইন্টিগ্রেশনটি স্বয়ংক্রিয়ভাবে আপনার সিস্টেমে ব্লুটুথ-সক্ষম মিডিয়া প্লেয়ারগুলি আবিষ্কার করবে।
3.  ড্রপডাউন তালিকা থেকে আপনার লক্ষ্য ডিভাইসটি (যেমন, "Xiaomi Mi Box 4") নির্বাচন করুন।
4.  **"Submit"** ("জমা দিন") ক্লিক করুন।

এটাই! ইন্টিগ্রেশনটি আপনার মিডিয়া প্লেয়ারের সাথে লিঙ্ক করা একটি সুইচ তৈরি করবে।

### অ্যাডভান্সড সেটআপ (উন্নত সেটআপ)

যদি সহজ সেটআপ আপনার ডিভাইস খুঁজে না পায় বা যদি আপনাকে শুরু থেকেই উন্নত টাইমিং সেটিংস কনফিগার করতে হয় তবে এই পদ্ধতিটি ব্যবহার করুন।

1.  **ধাপ 1: ডিভাইস নির্বাচন**
    - **"Advanced Setup"** ("অ্যাডভান্সড সেটআপ") বেছে নিন।
    - আপনার হোম অ্যাসিস্ট্যান্ট-এর *সমস্ত* মিডিয়া প্লেয়ারের তালিকা থেকে আপনার লক্ষ্য মিডিয়া প্লেয়ারটি নির্বাচন করুন।
2.  **ধাপ 2: MAC অ্যাড্রেস**
    - ইন্টিগ্রেশনটি নির্বাচিত ডিভাইসটির ব্লুটুথ MAC অ্যাড্রেস খুঁজে বের করার চেষ্টা করবে। 
    - যদি পাওয়া যায়, তবে এটি পূর্ব-পূরণ করা হবে। এটি সঠিক কিনা তা যাচাই করুন।
    - যদি খুঁজে না পাওয়া যায়, তবে আপনাকে আপনার ডিভাইসের ব্লুটুথ MAC অ্যাড্রেসটি ম্যানুয়ালি প্রবেশ করতে হবে।
3.  **ধাপ 3: টাইমিং সেটিংস**
    - আপনি ব্লুটুথ কমান্ডগুলির জন্য বিভিন্ন টাইমআউট এবং ডিলে কনফিগার করতে পারেন। বেশিরভাগ ব্যবহারকারীর জন্য, ডিফল্ট মানগুলি যথেষ্ট।
4.  সেটআপ সম্পূর্ণ করতে **"Submit"** ("জমা দিন") ক্লিক করুন।

## অপশন

একবার আপনি আপনার MiPower সুইচ কনফিগার করার পরে, আপনি যে কোনো সময় টাইমিং সেটিংস সামঞ্জস্য করতে পারেন।

1.  **Settings > Devices & Services** (সেটিংস > ডিভাইস এবং পরিষেবা) এ যান।
2.  MiPower ইন্টিগ্রেশনটি খুঁজুন এবং **"Configure"** ("কনফিগার করুন") ক্লিক করুন।
3.  প্রয়োজন অনুসারে ডিবাউন্স, টাইমআউট এবং ডিলেগুলির জন্য স্লাইডারগুলি সামঞ্জস্য করুন।

## টাইমিং সেটিংস ব্যাখ্যা

কনফিগারেশন বা অপশন মেনুতে, আপনি ব্লুটুথ কমান্ডগুলির টাইমিং সূক্ষ্মভাবে টিউন করতে পারেন। বেশিরভাগ ব্যবহারকারীর জন্য, ডিফল্ট মানগুলি ভাল কাজ করে।

- **Turn-On Debounce (চালু করার ডিবাউন্স):** 'চালু করার' কমান্ডটি আবার কার্যকর হওয়ার আগে যে ন্যূনতম সময় (সেকেন্ডে) অতিবাহিত হতে হবে। সুইচটি দ্রুত টগল করা হলে এটি ডিভাইসটিকে ওয়েক-আপ সিগন্যাল দিয়ে স্প্যাম করা থেকে বিরত রাখে।

- **Turn-Off Debounce (বন্ধ করার ডিবাউন্স):** 'বন্ধ করার' কমান্ডটি আবার কার্যকর হওয়ার আগে যে ন্যূনতম সময় (সেকেন্ডে) অতিবাহিত হতে হবে। 

- **Delay Between Commands (কমান্ডের মধ্যে বিলম্ব):** `bluetoothctl` ইউটিলিটিতে পরপর কমান্ড পাঠানোর মধ্যে একটি খুব সংক্ষিপ্ত বিলম্ব (সেকেন্ডে)। কিছু সিস্টেমে, একটি ছোট বিরতি যোগ করা নির্ভরযোগ্যতা উন্নত করতে পারে।

- **Process Spawn Timeout (প্রক্রিয়া শুরু হওয়ার টাইমআউট):** `bluetoothctl` প্রক্রিয়াটি শুরু হওয়ার জন্য অপেক্ষা করার সর্বাধিক সময় (সেকেন্ডে)। যদি এটি এই সময়ের মধ্যে শুরু হতে ব্যর্থ হয়, তবে চালু করার প্রচেষ্টা ব্যর্থ হবে।

- **Pairing Timeout (পেয়ারিং টাইমআউট):** সরলীকৃত টার্ন-অন লজিকে, এটি হল `pair` কমান্ড পাঠানোর পরে সফল হয়েছে বলে ধরে নেওয়ার আগে অপেক্ষা করার সময়। এটি ডিভাইসটিকে ওয়েক-আপ সিগনাল প্রক্রিয়া করার জন্য সময় দেয়।

- **Bluetooth Scan Duration (ব্লুটুথ স্ক্যান সময়কাল):** পেয়ার কমান্ড পাঠানোর চেষ্টা করার আগে ইন্টিগ্রেশনটি ব্লুটুথ ডিভাইসগুলির জন্য যে সময়কাল (সেকেন্ডে) স্ক্যান করবে। একটি দীর্ঘ স্ক্যান তাদের উপস্থিতির বিজ্ঞাপন দিতে ধীর এমন ডিভাইসগুলি খুঁজে পেতে সহায়তা করতে পারে।

## আপনার নিজের ভাষায় পড়ুন

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