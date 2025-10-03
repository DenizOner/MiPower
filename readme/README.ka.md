# MiPower — Home Assistant-ის მორგებული ინტეგრაცია

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** არის Home Assistant ინტეგრაცია, რომელიც საშუალებას გაძლევთ გააკონტროლოთ მედია ფლეერების ენერგიის სტატუსი, რომლებიც არ უჭერენ მხარს ტრადიციულ Wake-on-LAN (WOL)-ს, მაგრამ შეიძლება „გამოიღვიძონ“ Bluetooth-ის დაწყვილების მოთხოვნით. იგი სპეციალურად შეიქმნა ისეთი მოწყობილობებისთვის, როგორიცაა Xiaomi Mi Box, მაგრამ შეიძლება იმუშაოს სხვა მსგავს Android TV ყუთებთანაც.

ეს ინტეგრაცია ქმნის `switch` (გამრთველი) ერთეულს Home Assistant-ში. 
- გამრთველის **ჩართვა** აგზავნის Bluetooth ბრძანებების სერიას `bluetoothctl`-ის საშუალებით მოწყობილობის გასაღვიძებლად.
- გამრთველის **გამორთვა** იძახებს `media_player.turn_off` სერვისს დაკავშირებული მოწყობილობისთვის.
- გამრთველის მდგომარეობა ავტომატურად სინქრონიზდება დაკავშირებული მედია ფლეერის ერთეულის მდგომარეობასთან.

## 🤝 მხარდაჭერა

MiPower პროექტი ვითარდება ღია კოდის საზოგადოებისთვის ღირებულების დამატების ხედვით. თქვენი მხარდაჭერა სასიცოცხლოდ მნიშვნელოვანია ამ პროექტის უწყვეტობისა და განვითარების ტემპის შესანარჩუნებლად.

თუ აფასებთ ჩემს შრომას, შეგიძლიათ მხარი დამიჭიროთ GitHub Sponsors-ის ან შემდეგი პლატფორმების მეშვეობით. მადლობა წინასწარ!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

ალტერნატიულად, თქვენ შეგიძლიათ ნახოთ დაფინანსების ყველა ვარიანტი საცავის ზედა მარჯვენა კუთხეში **სპონსორის ღილაკზე (❤️)** დაწკაპუნებით.

## წინაპირობები

- **Home Assistant OS / Supervised / Container:** ეს ინტეგრაცია მოითხოვს Linux-ზე დაფუძნებულ Home Assistant-ის ინსტალაციას, სადაც `bluetoothctl` ბრძანების ხაზის ინსტრუმენტი ხელმისაწვდომია. ის **არ** იმუშავებს Home Assistant Core-ის ინსტალაციაზე Windows-ზე.

## ინსტალაცია HACS-ის საშუალებით (რეკომენდებულია)

ეს ინტეგრაცია ხელმისაწვდომია HACS-ში, როგორც მორგებული საცავი.

1.  გადადით თქვენს HACS დაფაზე.
2.  დააწკაპუნეთ **Integrations** (ინტეგრაციები).
3.  დააწკაპუნეთ სამ წერტილოვან მენიუზე ზედა მარჯვენა კუთხეში და აირჩიეთ **"Custom repositories"** ("მორგებული საცავები").
4.  დიალოგურ ფანჯარაში შეიყვანეთ შემდეგი ინფორმაცია:
    - **Repository (საცავი):** `https://github.com/DenizOner/MiPower`
    - **Category (კატეგორია):** `Integration` (ინტეგრაცია)
5.  დააწკაპუნეთ **"Add"** ("დამატება").
6.  "MiPower" ინტეგრაცია ახლა გამოჩნდება თქვენს HACS სიაში. დააწკაპუნეთ მასზე.
7.  დააწკაპუნეთ **"Download"** ("ჩამოტვირთვა") ღილაკზე და შემდეგ ისევ დააწკაპუნეთ **"Download"** ("ჩამოტვირთვა") შემდეგ ფანჯარაში.
8.  ჩამოტვირთვის დასრულების შემდეგ, **თქვენ უნდა გადატვირთოთ Home Assistant** ინტეგრაციის ჩასატვირთად.

## ხელით ინსტალაცია

მიუხედავად იმისა, რომ HACS არის რეკომენდებული მეთოდი, შეგიძლიათ ინტეგრაცია ხელითაც დააინსტალიროთ.

1.  გადადით საცავის [გამოშვებების გვერდზე](https://github.com/DenizOner/MiPower/releases) და ჩამოტვირთეთ `mipower.zip` ფაილი უახლესი გამოშვებიდან.
2.  ამოიღეთ (unzip) გადმოწერილი ფაილი.
3.  ამოღებული საქაღალდის შიგნით ნახავთ `custom_components` დირექტორიას. დააკოპირეთ `mipower` საქაღალდე მისგან.
4.  ჩასვით კოპირებული `mipower` საქაღალდე `custom_components` საქაღალდეში თქვენს Home Assistant კონფიგურაციის დირექტორიაში. თუ `custom_components` საქაღალდე არ არსებობს, უნდა შექმნათ იგი.
    - საბოლოო გზა ასე უნდა გამოიყურებოდეს: `.../config/custom_components/mipower/`
5.  გადატვირთეთ Home Assistant.

## კონფიგურაცია

გადატვირთვის შემდეგ, შეგიძლიათ დაამატოთ და დააკონფიგურიროთ MiPower გამრთველი.

1.  გადადით **Settings > Devices & Services** (პარამეტრები > მოწყობილობები და სერვისები).
2.  დააწკაპუნეთ **"+ Add Integration"** ("+ ინტეგრაციის დამატება") ღილაკზე ქვედა მარჯვენა კუთხეში.
3.  მოძებნეთ **"MiPower"** და დააწკაპუნეთ მასზე.

### მარტივი დაყენება (რეკომენდებულია)

ეს არის ინტეგრაციის კონფიგურაციის უმარტივესი გზა.

1.  მოთხოვნისას, აირჩიეთ **"Easy Setup"** ("მარტივი დაყენება").
2.  ინტეგრაცია ავტომატურად აღმოაჩენს Bluetooth-ით ჩართულ მედია ფლეერებს თქვენს სისტემაში.
3.  აირჩიეთ თქვენი სამიზნე მოწყობილობა (მაგ. "Xiaomi Mi Box 4") ჩამოსაშლელი სიიდან.
4.  დააწკაპუნეთ **"Submit"** ("გაგზავნა").

სულ ეს არის! ინტეგრაცია შექმნის თქვენს მედია ფლეერთან დაკავშირებულ გამრთველს.

### მოწინავე დაყენება

გამოიყენეთ ეს მეთოდი, თუ მარტივი დაყენება ვერ პოულობს თქვენს მოწყობილობას ან თუ თავიდანვე გჭირდებათ მოწინავე დროის პარამეტრების კონფიგურაცია.

1.  **ნაბიჯი 1: მოწყობილობის არჩევა**
    - აირჩიეთ **"Advanced Setup"** ("მოწინავე დაყენება").
    - აირჩიეთ თქვენი სამიზნე მედია ფლეერი თქვენს Home Assistant-ში არსებული *ყველა* მედია ფლეერის სიიდან.
2.  **ნაბიჯი 2: MAC მისამართი**
    - ინტეგრაცია შეეცდება იპოვოს არჩეული მოწყობილობის Bluetooth MAC მისამართი. 
    - თუ მოიძებნა, ის წინასწარ შეივსება. დაადასტურეთ, რომ ის სწორია.
    - თუ ვერ მოიძებნა, ხელით უნდა შეიყვანოთ თქვენი მოწყობილობის Bluetooth MAC მისამართი.
3.  **ნაბიჯი 3: დროის პარამეტრები**
    - შეგიძლიათ დააკონფიგურიროთ სხვადასხვა დროის ლიმიტი და დაყოვნება Bluetooth ბრძანებებისთვის. მომხმარებლების უმეტესობისთვის ნაგულისხმევი მნიშვნელობები საკმარისია.
4.  დააწკაპუნეთ **"Submit"** ("გაგზავნა") დაყენების დასასრულებლად.

## პარამეტრები

MiPower გამრთველის კონფიგურაციის შემდეგ, შეგიძლიათ დროის პარამეტრების რეგულირება ნებისმიერ დროს.

1.  გადადით **Settings > Devices & Services** (პარამეტრები > მოწყობილობები და სერვისები).
2.  იპოვეთ MiPower ინტეგრაცია და დააწკაპუნეთ **"Configure"** ("კონფიგურაცია").
3.  საჭიროებისამებრ დაარეგულირეთ სლაიდერები *debounce*, დროის ლიმიტებისა და დაყოვნებებისთვის.

## დროის პარამეტრების ახსნა

კონფიგურაციის ან პარამეტრების მენიუში შეგიძლიათ დახვეწოთ Bluetooth ბრძანებების დრო. მომხმარებლების უმეტესობისთვის ნაგულისხმევი მნიშვნელობები კარგად მუშაობს.

- **Turn-On Debounce (ჩართვის შეყოვნება):** მინიმალური დრო (წამებში), რომელიც უნდა გავიდეს, სანამ 'ჩართვის' ბრძანება ხელახლა შესრულდება. ეს ხელს უშლის მოწყობილობის გაღვიძების სიგნალებით "გასპამებას", თუ გამრთველი სწრაფად ირთვება.

- **Turn-Off Debounce (გამორთვის შეყოვნება):** მინიმალური დრო (წამებში), რომელიც უნდა გავიდეს, სანამ 'გამორთვის' ბრძანება ხელახლა შესრულდება. 

- **Delay Between Commands (დაყოვნება ბრძანებებს შორის):** ძალიან მოკლე დაყოვნება (წამებში) `bluetoothctl` უტილიტაში თანმიმდევრული ბრძანებების გაგზავნას შორის. ზოგიერთ სისტემაზე, მცირე პაუზის დამატებამ შეიძლება გააუმჯობესოს საიმედოობა.

- **Process Spawn Timeout (პროცესის გაშვების დროის ლიმიტი):** მაქსიმალური დრო (წამებში) `bluetoothctl` პროცესის დაწყების მოლოდინში. თუ ამ დროის განმავლობაში ის ვერ დაიწყებს, ჩართვის მცდელობა ჩაიშლება.

- **Pairing Timeout (დაწყვილების დროის ლიმიტი):** გამარტივებულ ჩართვის ლოგიკაში, ეს არის დრო, რომელიც უნდა დაელოდოთ `pair` ბრძანების გაგზავნის შემდეგ, სანამ წარმატება ჩაითვლება. ეს აძლევს მოწყობილობას დროს, რომ დაამუშაოს გაღვიძების სიგნალი.

- **Bluetooth Scan Duration (Bluetooth სკანირების ხანგრძლივობა):** ხანგრძლივობა (წამებში), რომლის განმავლობაშიც ინტეგრაცია დაასკანირებს Bluetooth მოწყობილობებს, სანამ დაწყვილების ბრძანების გაგზავნას შეეცდება. უფრო ხანგრძლივი სკანირება დაგეხმარებათ იპოვოთ მოწყობილობები, რომლებიც ნელა აცხადებენ თავიანთ ყოფნას.

## წაიკითხეთ თქვენს ენაზე

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