# MiPower — Home Assistant pasgemaakte integrasie

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** is 'n Home Assistant-integrasie wat jou toelaat om die kragtoestand van mediaspelers te beheer wat nie tradisionele Wake-on-LAN (WOL) ondersteun nie, maar wat "wakker gemaak" kan word deur 'n Bluetooth-paringversoek. Dit is spesifiek ontwerp vir toestelle soos die Xiaomi Mi Box, maar kan met ander soortgelyke Android TV-bokse werk.

Hierdie integrasie skep 'n `switch`-entiteit in Home Assistant. 
- **Aanskakel** van die skakelaar stuur 'n reeks Bluetooth-opdragte via `bluetoothctl` om die toestel wakker te maak.
- **Afskakel** van die skakelaar roep die `media_player.turn_off`-diens vir die gekoppelde toestel.
- Die toestand van die skakelaar word outomaties gesinchroniseer met die toestand van die gekoppelde mediaspeler-entiteit.

## 🤝 Ondersteun

Die MiPower-projek word ontwikkel met die visie om waarde tot die oopbron-gemeenskap toe te voeg. U ondersteuning is van kardinale belang om die volhoubaarheid en ontwikkelingspoed van hierdie projek te handhaaf.

As u my werk waardeer, kan u my ondersteun via GitHub Sponsors of die volgende platforms. Dankie by voorbaat!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatiewelik, kan u al die finansieringsopsies sien deur op die **Borg-knoppie (❤️)** in die regter boonste hoek van die bewaarplek te klik.

## Voorvereistes

- **Home Assistant OS / Supervised / Container:** Hierdie integrasie vereis 'n Linux-gebaseerde Home Assistant-installasie waar die `bluetoothctl`-opdraglyn-instrument beskikbaar en toeganklik is. Dit sal **nie** werk op 'n Home Assistant Core-installasie op Windows nie.

## Installasie via HACS (Aanbeveel)

Hierdie integrasie is beskikbaar as 'n pasgemaakte bewaarplek in HACS.

1.  Navigeer na jou HACS-kontroleskerm.
2.  Klik op **Integrations** (Integrasies).
3.  Klik op die driekolletjies-kieslys in die regter boonste hoek en kies **"Custom repositories"** ("Pasgemaakte bewaarplekke").
4.  In die dialoogkassie, voer die volgende inligting in:
    - **Repository (Bewaarplek):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorie):** `Integration` (Integrasie)
5.  Klik **"Add"** ("Voeg by").
6.  Die "MiPower"-integrasie sal nou in jou HACS-lys verskyn. Klik daarop.
7.  Klik die **"Download"** ("Aflaai")-knoppie en dan weer **"Download"** ("Aflaai") in die volgende venster.
8.  Nadat die aflaai voltooi is, **moet** jy **Home Assistant herbegin** sodat die integrasie gelaai kan word.

## Handmatige Installasie

Alhoewel HACS die aanbevole metode is, kan jy die integrasie ook handmatig installeer.

1.  Gaan na die [Releases-bladsy](https://github.com/DenizOner/MiPower/releases) van die bewaarplek en laai die `mipower.zip`-lêer van die nuutste vrystelling af.
2.  Pak die afgelaaide lêer uit.
3.  Binne die uitgepakte lêergids sal jy 'n `custom_components`-gids vind. Kopieer die `mipower`-lêergids daaruit.
4.  Plak die gekopieerde `mipower`-lêergids in die `custom_components`-lêergids in jou Home Assistant-konfigurasiegids. As die `custom_components`-lêergids nie bestaan nie, moet jy dit skep.
    - Die finale pad moet lyk soos: `.../config/custom_components/mipower/`
5.  Herbegin Home Assistant.

## Konfigurasie

Na die herbegin, kan jy die MiPower-skakelaar byvoeg en konfigureer.

1.  Gaan na **Settings > Devices & Services** (Instellings > Toestelle & Dienste).
2.  Klik die **"+ Add Integration"** ("+ Voeg Integrasie by")-knoppie in die regter onderste hoek.
3.  Soek vir **"MiPower"** en klik daarop.

### Maklike Opstelling (Aanbeveel)

Dit is die eenvoudigste manier om die integrasie te konfigureer.

1.  Wanneer gevra, kies **"Easy Setup"** ("Maklike Opstelling").
2.  Die integrasie sal outomaties Bluetooth-geaktiveerde mediaspelers op jou stelsel ontdek.
3.  Kies jou teikentoestel (bv. "Xiaomi Mi Box 4") uit die aftreklys.
4.  Klik **"Submit"** ("Stuur in").

Dis dit! Die integrasie sal 'n skakelaar skep wat aan jou mediaspeler gekoppel is.

### Gevorderde Opstelling

Gebruik hierdie metode as die Maklike Opstelling nie jou toestel vind nie of as jy gevorderde tydsberekening-instellings van die begin af moet konfigureer.

1.  **Stap 1: Toestelkeuse**
    - Kies **"Advanced Setup"** ("Gevorderde Opstelling").
    - Kies jou teiken mediaspeler uit die lys van *alle* mediaspelers in jou Home Assistant.
2.  **Stap 2: MAC-adres**
    - Die integrasie sal probeer om die Bluetooth MAC-adres van die geselekteerde toestel te vind. 
    - Indien gevind, sal dit vooraf ingevul wees. Verifieer dat dit korrek is.
    - Indien nie gevind nie, moet jy die Bluetooth MAC-adres van jou toestel handmatig invoer.
3.  **Stap 3: Tydsberekening-instellings**
    - Jy kan verskeie uittye en vertragings vir die Bluetooth-opdragte konfigureer. Vir die meeste gebruikers is die verstekwaardes voldoende.
4.  Klik **"Submit"** ("Stuur in") om die opstelling te voltooi.

## Opsies

Nadat jy jou MiPower-skakelaar gekonfigureer het, kan jy die tydsberekening-instellings enige tyd aanpas.

1.  Gaan na **Settings > Devices & Services** (Instellings > Toestelle & Dienste).
2.  Vind die MiPower-integrasie en klik **"Configure"** ("Konfigureer").
3.  Pas die skuifknoppies vir debons, uittye en vertragings aan soos benodig.

## Tydsberekening-instellings Verduidelik

In die konfigurasie- of opsies-kieslys kan jy die tydsberekening van die Bluetooth-opdragte fyninstel. Vir die meeste gebruikers werk die verstekwaardes goed.

- **Turn-On Debounce (Aanskakel Debons):** Die minimum tyd (in sekondes) wat moet verloop voordat die 'aanskakel'-opdrag weer uitgevoer kan word. Dit voorkom die strooipos van die toestel met wakkermaak-seine as die skakelaar vinnig geskakel word.

- **Turn-Off Debounce (Afskakel Debons):** Die minimum tyd (in sekondes) wat moet verloop voordat die 'afskakel'-opdrag weer uitgevoer kan word. 

- **Delay Between Commands (Vertraging Tussen Opdragte):** 'n Baie kort vertraging (in sekondes) tussen die stuur van opeenvolgende opdragte na die `bluetoothctl`-hulpprogram. Op sommige stelsels kan die byvoeging van 'n klein pouse betroubaarheid verbeter.

- **Process Spawn Timeout (Proses Opwek Tydsuittyd):** Die maksimum tyd (in sekondes) om te wag vir die `bluetoothctl`-proses om te begin. As dit misluk om binne hierdie tyd te begin, sal die aanskakel-poging misluk.

- **Pairing Timeout (Paring Tydsuittyd):** In die vereenvoudigde aanskakel-logika, is dit die hoeveelheid tyd om te wag nadat die `pair`-opdrag gestuur is voordat sukses aanvaar word. Dit gee die toestel tyd om die wakkermaak-sein te verwerk.

- **Bluetooth Scan Duration (Bluetooth Skandeer Duur):** Die duur (in sekondes) wat die integrasie sal skandeer vir Bluetooth-toestelle voordat gepoog word om die paring-opdrag te stuur. 'n Langer skandering kan help om toestelle te vind wat stadig is om hul teenwoordigheid te adverteer.

## Lees in u eie taal

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