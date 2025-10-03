# MiPower — Прилагођена интеграција за Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** је интеграција за Home Assistant која вам омогућава да контролишете стање напајања медија плејера који не подржавају традиционални Wake-on-LAN (WOL), али се могу „пробудити“ захтевом за упаривање преко Bluetooth-а. Специјално је дизајнирана за уређаје као што је Xiaomi Mi Box, али може радити и са другим сличним Android TV боксовима.

Ова интеграција креира `switch` (прекидач) ентитет у Home Assistant-у. 
- **Укључивање** прекидача шаље низ Bluetooth команди преко `bluetoothctl` да пробуди уређај.
- **Искључивање** прекидача позива услугу `media_player.turn_off` за повезани уређај.
- Стање прекидача се аутоматски синхронизује са стањем ентитета повезаног медија плејера.

## 🤝 Подржите нас

Пројекат MiPower се развија са визијом додавања вредности заједници отвореног кода. Ваша подршка је од виталног значаја за одржавање континуитета и брзине развоја овог пројекта.

Ако цените мој рад, можете ме подржати преко GitHub Спонзора или следећих платформи. Хвала унапред!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Алтернативно, све опције финансирања можете видети кликом на **дугме Спонзор (❤️)** у горњем десном углу спремишта.

## Предуслови

- **Home Assistant OS / Supervised / Container:** Ова интеграција захтева инсталацију Home Assistant-а базирану на Linux-у, где је алат командне линије `bluetoothctl` доступан и приступачан. **НЕЋЕ** радити на инсталацији Home Assistant Core-а на Windows-у.

## Инсталација преко HACS-а (Препоручено)

Ова интеграција је доступна као прилагођени репозиторијум у HACS-у.

1.  Идите на своју HACS контролну таблу.
2.  Кликните на **Integrations** (Интеграције).
3.  Кликните на мени са три тачке у горњем десном углу и изаберите **"Custom repositories"** ("Прилагођени репозиторијуми").
4.  У дијалог боксу унесите следеће информације:
    - **Repository (Репозиторијум):** `https://github.com/DenizOner/MiPower`
    - **Category (Категорија):** `Integration` (Интеграција)
5.  Кликните на **"Add"** ("Додај").
6.  Интеграција "MiPower" ће се сада појавити на вашој HACS листи. Кликните на њу.
7.  Кликните на дугме **"Download"** ("Преузми"), а затим поново **"Download"** ("Преузми") у следећем прозору.
8.  Након што се преузимање заврши, **МОРАТЕ поново покренути Home Assistant** да би се интеграција учитала.

## Ручна инсталација

Иако је HACS препоручени метод, интеграцију можете инсталирати и ручно.

1.  Идите на [страницу издања](https://github.com/DenizOner/MiPower/releases) репозиторијума и преузмите датотеку `mipower.zip` из најновијег издања.
2.  Распакујте преузету датотеку.
3.  Унутар распаковане фасцикле, наћи ћете директоријум `custom_components`. Копирајте фасциклу `mipower` из њега.
4.  Налепите копирану фасциклу `mipower` у фасциклу `custom_components` у вашем конфигурационом директоријуму Home Assistant-а. Ако фасцикла `custom_components` не постоји, морате је креирати.
    - Коначна путања би требало да изгледа овако: `.../config/custom_components/mipower/`
5.  Поново покрените Home Assistant.

## Конфигурација

Након поновног покретања, можете додати и конфигурисати MiPower прекидач.

1.  Идите на **Settings > Devices & Services** (Подешавања > Уређаји и Услуге).
2.  Кликните на дугме **"+ Add Integration"** ("+ Додај Интеграцију") у доњем десном углу.
3.  Претражите **"MiPower"** и кликните на њега.

### Једноставна конфигурација (Препоручено)

Ово је најједноставнији начин за конфигурисање интеграције.

1.  Када се затражи, изаберите **"Easy Setup"** ("Једноставна Конфигурација").
2.  Интеграција ће аутоматски открити медија плејере са омогућеним Bluetooth-ом на вашем систему.
3.  Изаберите свој циљни уређај (нпр. "Xiaomi Mi Box 4") са падајуће листе.
4.  Кликните на **"Submit"** ("Пошаљи").

То је то! Интеграција ће креирати прекидач повезан са вашим медија плејером.

### Напредна конфигурација

Користите ову методу ако Једноставна конфигурација не пронађе ваш уређај или ако морате да конфигуришете напредна подешавања времена од почетка.

1.  **Корак 1: Избор уређаја**
    - Изаберите **"Advanced Setup"** ("Напредна Конфигурација").
    - Изаберите свој циљни медија плејер са листе *свих* медија плејера у вашем Home Assistant-у.
2.  **Корак 2: MAC адреса**
    - Интеграција ће покушати да пронађе Bluetooth MAC адресу одабраног уређаја. 
    - Ако се пронађе, биће унапред попуњена. Проверите да ли је тачна.
    - Ако се не пронађе, морате ручно унети Bluetooth MAC адресу свог уређаја.
3.  **Корак 3: Подешавања времена**
    - Можете конфигурисати различите временске периоде и кашњења за Bluetooth команде. За већину корисника, подразумеване вредности су довољне.
4.  Кликните на **"Submit"** ("Пошаљи") да бисте довршили подешавање.

## Опције

Након што конфигуришете свој MiPower прекидач, можете у било ком тренутку прилагодити подешавања времена.

1.  Идите на **Settings > Devices & Services** (Подешавања > Уређаји и Услуге).
2.  Пронађите MiPower интеграцију и кликните **"Configure"** ("Конфигуриши").
3.  Подесите клизаче за *debounce*, временске периоде и кашњења по потреби.

## Објашњење подешавања времена

У менију за конфигурацију или опције, можете фино подесити време Bluetooth команди. За већину корисника, подразумеване вредности добро функционишу.

- **Turn-On Debounce (Поништавање грешке при укључивању):** Минимално време (у секундама) које мора да прође пре него што се команда „укључи“ може поново извршити. Ово спречава слање нежељених сигнала за буђење уређају ако се прекидач брзо пребацује.

- **Turn-Off Debounce (Поништавање грешке при искључивању):** Минимално време (у секундама) које мора да прође пре него што се команда „искључи“ може поново извршити. 

- **Delay Between Commands (Кашњење између команди):** Врло кратко кашњење (у секундама) између слања узастопних команди алату `bluetoothctl`. На неким системима, додавање мале паузе може побољшати поузданост.

- **Process Spawn Timeout (Временски период покретања процеса):** Максимално време (у секундама) чекања да се покрене процес `bluetoothctl`. Ако се не покрене у овом року, покушај укључивања неће успети.

- **Pairing Timeout (Временски период упаривања):** У поједностављеној логици укључивања, ово је време чекања након слања команде `pair` пре него што се претпостави успех. Даје уређају времена да обради сигнал за буђење.

- **Bluetooth Scan Duration (Трајање Bluetooth скенирања):** Трајање (у секундама) током којег ће интеграција скенирати Bluetooth уређаје пре него што покуша да пошаље команду за упаривање. Дуже скенирање може помоћи у проналажењу уређаја који споро оглашавају своје присуство.

## Читајте на свом језику

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