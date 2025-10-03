# MiPower — Персонализирана интеграция за Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** е интеграция за Home Assistant, която ви позволява да контролирате състоянието на захранването на мултимедийни плейъри, които не поддържат традиционното Wake-on-LAN (WOL), но могат да бъдат "събудени" чрез заявка за Bluetooth сдвояване. Тя е специално проектирана за устройства като Xiaomi Mi Box, но може да работи и с други подобни Android TV боксове.

Тази интеграция създава `switch` (превключвател) обект в Home Assistant. 
- **Включването** на превключвателя изпраща поредица от Bluetooth команди чрез `bluetoothctl` за събуждане на устройството.
- **Изключването** на превключвателя извиква услугата `media_player.turn_off` за свързаното устройство.
- Състоянието на превключвателя автоматично се синхронизира със състоянието на свързания обект мултимедиен плейър.

## 🤝 Подкрепете ни

Проектът MiPower се разработва с визия за добавяне на стойност към общността с отворен код. Вашата подкрепа е жизненоважна за поддържане на непрекъснатостта и скоростта на развитие на този проект.

Ако оценявате работата ми, можете да ме подкрепите чрез GitHub Sponsors или следните платформи. Благодаря предварително!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Като алтернатива, можете да видите всички опции за финансиране, като щракнете върху **бутона Спонсор (❤️)** в горния десен ъгъл на хранилището.

## Предварителни изисквания

- **Home Assistant OS / Supervised / Container:** Тази интеграция изисква инсталация на Home Assistant, базирана на Linux, където инструментът за команден ред `bluetoothctl` е наличен и достъпен. Тя **няма** да работи на Home Assistant Core инсталация под Windows.

## Инсталиране чрез HACS (Препоръчително)

Тази интеграция е достъпна като персонализирано хранилище в HACS.

1.  Отидете до вашето HACS табло за управление.
2.  Кликнете върху **Integrations** (Интеграции).
3.  Кликнете върху менюто с три точки в горния десен ъгъл и изберете **"Custom repositories"** ("Персонализирани хранилища").
4.  В диалоговия прозорец въведете следната информация:
    - **Repository (Хранилище):** `https://github.com/DenizOner/MiPower`
    - **Category (Категория):** `Integration` (Интеграция)
5.  Кликнете **"Add"** ("Добавяне").
6.  Интеграцията "MiPower" вече ще се появи във вашия HACS списък. Кликнете върху нея.
7.  Кликнете върху бутона **"Download"** ("Изтегляне") и след това отново **"Download"** ("Изтегляне") в следващия прозорец.
8.  След като изтеглянето приключи, **трябва да рестартирате Home Assistant**, за да бъде заредена интеграцията.

## Ръчна инсталация

Въпреки че HACS е препоръчителният метод, можете да инсталирате интеграцията и ръчно.

1.  Отидете на [страницата с издания](https://github.com/DenizOner/MiPower/releases) на хранилището и изтеглете файла `mipower.zip` от най-новото издание.
2.  Разархивирайте изтегления файл.
3.  Вътре в разархивираната папка ще намерите директория `custom_components`. Копирайте папката `mipower` от нея.
4.  Поставете копираната папка `mipower` в папката `custom_components` във вашата конфигурационна директория на Home Assistant. Ако папката `custom_components` не съществува, трябва да я създадете.
    - Крайният път трябва да изглежда така: `.../config/custom_components/mipower/`
5.  Рестартирайте Home Assistant.

## Конфигурация

След рестартирането можете да добавите и конфигурирате превключвателя MiPower.

1.  Отидете на **Settings > Devices & Services** (Настройки > Устройства и Услуги).
2.  Кликнете върху бутона **"+ Add Integration"** ("+ Добавяне на интеграция") в долния десен ъгъл.
3.  Потърсете **"MiPower"** и кликнете върху него.

### Лесна настройка (Препоръчително)

Това е най-лесният начин за конфигуриране на интеграцията.

1.  Когато бъдете подканени, изберете **"Easy Setup"** ("Лесна настройка").
2.  Интеграцията автоматично ще открие мултимедийни плейъри с Bluetooth на вашата система.
3.  Изберете вашето целево устройство (напр. "Xiaomi Mi Box 4") от падащия списък.
4.  Кликнете **"Submit"** ("Изпращане").

Това е! Интеграцията ще създаде превключвател, свързан с вашия мултимедиен плейър.

### Разширена настройка

Използвайте този метод, ако Лесната настройка не намери вашето устройство или ако трябва да конфигурирате разширени настройки за време още от самото начало.

1.  **Стъпка 1: Избор на устройство**
    - Изберете **"Advanced Setup"** ("Разширена настройка").
    - Изберете вашия целеви мултимедиен плейър от списъка с *всички* мултимедийни плейъри във вашия Home Assistant.
2.  **Стъпка 2: MAC адрес**
    - Интеграцията ще се опита да намери Bluetooth MAC адреса на избраното устройство. 
    - Ако бъде намерен, той ще бъде предварително попълнен. Проверете дали е правилен.
    - Ако не бъде намерен, трябва да въведете Bluetooth MAC адреса на вашето устройство ръчно.
3.  **Стъпка 3: Настройки за време**
    - Можете да конфигурирате различни изчаквания и закъснения за Bluetooth командите. За повечето потребители стойностите по подразбиране са достатъчни.
4.  Кликнете **"Submit"** ("Изпращане"), за да завършите настройката.

## Опции

След като сте конфигурирали вашия MiPower превключвател, можете да коригирате настройките за време по всяко време.

1.  Отидете на **Settings > Devices & Services** (Настройки > Устройства и Услуги).
2.  Намерете интеграцията MiPower и кликнете **"Configure"** ("Конфигуриране").
3.  Регулирайте плъзгачите за "debounce", изчаквания и закъснения според нуждите.

## Обяснение на настройките за време

В менюто за конфигуриране или опции можете да настроите фино времето на Bluetooth командите. За повечето потребители стойностите по подразбиране работят добре.

- **Turn-On Debounce (Забавяне на включването):** Минималното време (в секунди), което трябва да изтече, преди командата за „включване“ да може да бъде изпълнена отново. Това предотвратява изпращането на спам до устройството със сигнали за събуждане, ако превключвателят се превключва бързо.

- **Turn-Off Debounce (Забавяне на изключването):** Минималното време (в секунди), което трябва да изтече, преди командата за „изключване“ да може да бъде изпълнена отново. 

- **Delay Between Commands (Закъснение между командите):** Много кратко закъснение (в секунди) между изпращането на последователни команди към помощната програма `bluetoothctl`. В някои системи добавянето на малка пауза може да подобри надеждността.

- **Process Spawn Timeout (Изчакване за стартиране на процес):** Максималното време (в секунди) за изчакване на процеса `bluetoothctl` да започне. Ако не успее да стартира в рамките на това време, опитът за включване ще бъде неуспешен.

- **Pairing Timeout (Изчакване за сдвояване):** В опростената логика за включване, това е времето за изчакване след изпращане на командата `pair`, преди да се приеме успех. То дава на устройството време да обработи сигнала за събуждане.

- **Bluetooth Scan Duration (Продължителност на Bluetooth сканирането):** Продължителността (в секунди), през която интеграцията ще сканира за Bluetooth устройства, преди да опита да изпрати командата за сдвояване. По-дългото сканиране може да помогне за намирането на устройства, които бавно обявяват присъствието си.

## Прочетете на своя език

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