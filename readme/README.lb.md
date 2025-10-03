# MiPower — Home Assistant Custom Integratioun

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** ass eng Home Assistant Integratioun déi Iech erlaabt de Stroumstatus vu Mediaspilleren ze kontrolléieren déi traditionell Wake-on-LAN (WOL) net ënnerstëtzen, awer duerch eng Bluetooth Paartufro kënne "waakreg gemaach" ginn. Et gouf speziell fir Geräter wéi d'Xiaomi Mi Box entworf, kann awer och mat anere ähnleche Android TV Boxen funktionéieren.

Dës Integratioun erstellt eng `switch` (Schalter) Entitéit am Home Assistant. 
- De Schalter **ANzeschalten** schéckt eng Serie vu Bluetooth Kommandoen iwwer `bluetoothctl` fir den Apparat z'erwächen.
- De Schalter **AUSzeschalten** rifft de Service `media_player.turn_off` fir de verlinkten Apparat op.
- De Status vum Schalter gëtt automatesch mam Status vun der verlinkter Mediaspiller Entitéit synchroniséiert.

## 🤝 Ënnerstëtzt eis

De MiPower Projet gëtt entwéckelt mat der Visioun, Wäert an d'Open-Source Communautéit ze bréngen. Är Ënnerstëtzung ass vital fir d'Kontinuitéit an d'Entwécklungsgeschwindegkeet vun dësem Projet ze halen.

Wann Dir meng Aarbecht schätzt, kënnt Dir mech iwwer GitHub Sponsors oder déi folgend Plattforme ënnerstëtzen. Villmools Merci am Viraus!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativ kënnt Dir all Finanzéierungsoptioune gesinn andeems Dir op den **Sponsor Knäppchen (❤️)** am uewe rietsen Eck vum Repository klickt.

## Viraussetzungen

- **Home Assistant OS / Supervised / Container:** Dës Integratioun erfuerdert eng Linux-baséiert Home Assistant Installatioun, wou de `bluetoothctl` Kommandozeilentool verfügbar an zougänglech ass. Et wäert **net** op enger Home Assistant Core Installatioun op Windows funktionéieren.

## Installatioun iwwer HACS (Recommandéiert)

Dës Integratioun ass als personaliséierte Repository an HACS verfügbar.

1.  Navigéiert op Ären HACS Dashboard.
2.  Klickt op **Integrations** (Integratiounen).
3.  Klickt op den Dräi-Punkt Menü uewe riets a wielt **"Custom repositories"** ("Personaliséiert Repositories").
4.  Am Dialogfeld, gitt déi folgend Informatiounen an:
    - **Repository (Repository):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorie):** `Integration` (Integratioun)
5.  Klickt **"Add"** ("Derbäi setzen").
6.  D'"MiPower" Integratioun wäert elo op Ärer HACS Lëscht erschéngen. Klickt drop.
7.  Klickt op de Knäppchen **"Download"** ("Eroflueden") an dann nach eng Kéier op **"Download"** ("Eroflueden") an der nächster Fënster.
8.  Nodeems den Download fäerdeg ass, **musst Dir Home Assistant neistarten** fir d'Integratioun ze lueden.

## Manuell Installatioun

Och wann HACS déi recommandéiert Method ass, kënnt Dir d'Integratioun och manuell installéieren.

1.  Gitt op d'[Releases Säit](https://github.com/DenizOner/MiPower/releases) vum Repository a luet de Fichier `mipower.zip` vun der leschter Versioun erof.
2.  Pak de erofgeluedenen Fichier aus.
3.  Bannent dem ausgepaakten Dossier fannt Dir en `custom_components` Verzeechnes. Kopéiert den Dossier `mipower` dovun.
4.  Paste den kopéierten `mipower` Dossier an den `custom_components` Dossier an Ärem Home Assistant Konfiguratiounsverzeechnes. Wann den `custom_components` Dossier net existéiert, musst Dir en erstellen.
    - De finalen Wee soll esou ausgesinn: `.../config/custom_components/mipower/`
5.  Start Home Assistant nei.

## Konfiguratioun

Nom Neistart kënnt Dir de MiPower Schalter derbäisetzen a konfiguréieren.

1.  Gitt op **Settings > Devices & Services** (Astellungen > Geräter & Servicer).
2.  Klickt op de Knäppchen **"+ Add Integration"** ("+ Integratioun derbäisetzen") ënnen riets.
3.  Sich no **"MiPower"** a klickt drop.

### Einfach Setup (Recommandéiert)

Dëst ass den einfachste Wee fir d'Integratioun ze konfiguréieren.

1.  Wann Dir gefrot gitt, wielt **"Easy Setup"** ("Einfach Setup").
2.  D'Integratioun entdeckt automatesch Bluetooth-aktivéiert Mediaspiller op Ärem System.
3.  Wielt Ären Zilapparat (z.B. "Xiaomi Mi Box 4") aus der Dropdown-Lëscht.
4.  Klickt **"Submit"** ("Ofschécken").

Dat ass et! D'Integratioun erstellt e Schalter deen mat Ärem Mediaspiller verlinkt ass.

### Erweidert Setup

Benotzt dës Method wann den Einfache Setup Ären Apparat net fënnt oder wann Dir fortgeschratt Timing Astellunge vun Ufank un konfiguréiere musst.

1.  **Schrëtt 1: Apparat Auswiel**
    - Wielt **"Advanced Setup"** ("Erweidert Setup").
    - Wielt Ären Zil Mediaspiller aus der Lëscht vun *allen* Mediaspilleren an Ärem Home Assistant.
2.  **Schrëtt 2: MAC Adress**
    - D'Integratioun probéiert d'Bluetooth MAC Adress vum gewielten Apparat ze fannen. 
    - Wann et fonnt gëtt, gëtt et virgefëllt. Verifizéiert datt et richteg ass.
    - Wann net fonnt, musst Dir d'Bluetooth MAC Adress vun Ärem Apparat manuell aginn.
3.  **Schrëtt 3: Timing Astellungen**
    - Dir kënnt verschidden Timings an Delai'en fir d'Bluetooth Kommandoen konfiguréieren. Fir déi meescht Benotzer sinn d'Standardwäerter duer.
4.  Klickt **"Submit"** ("Ofschécken") fir de Setup ofzeschléissen.

## Optiounen

Wann Dir Äre MiPower Schalter konfiguréiert hutt, kënnt Dir d'Timing Astellungen zu all Moment upassen.

1.  Gitt op **Settings > Devices & Services** (Astellungen > Geräter & Servicer).
2.  Fannt d'MiPower Integratioun a klickt **"Configure"** ("Konfiguréieren").
3.  Passt d'Schieber fir *debounce*, Timings an Delai'en wéi néideg un.

## Erklärung vun den Timing Astellungen

Am Konfiguratiouns- oder Optiounsmenü kënnt Dir d'Timing vun de Bluetooth Kommandoen feinjustéieren. Fir déi meescht Benotzer funktionéieren d'Standardwäerter gutt.

- **Turn-On Debounce (Anschalt-Debounce):** Déi minimal Zäit (a Sekonnen) déi muss vergoen ier de Kommando 'aschalten' erëm ausgefouert ka ginn. Dëst verhënnert datt den Apparat mat Wakreg-Signaler gespammt gëtt wann de Schalter séier ëmgeschalt gëtt.

- **Turn-Off Debounce (Ausschalt-Debounce):** Déi minimal Zäit (a Sekonnen) déi muss vergoen ier de Kommando 'ausschalten' erëm ausgefouert ka ginn. 

- **Delay Between Commands (Delai tëscht Kommandoen):** E ganz kuerzen Delai (a Sekonnen) tëscht dem Schécken vu successive Kommandoen un den `bluetoothctl` Utility. Op e puer Systemer kann d'Zousetzung vun enger klenger Paus d'Zouverlässegkeet verbesseren.

- **Process Spawn Timeout (Prozess Start Timeout):** Déi maximal Zäit (a Sekonnen) fir ze waarden bis de `bluetoothctl` Prozess start. Wann en net bannent dëser Zäit start, wäert d'Anschalt-Versuch falen.

- **Pairing Timeout (Paart Timeout):** An der vereinfachter Anschalt-Logik ass dëst d'Zäit déi nom Schécken vum Kommando `pair` gewaart gëtt ier Erfolleg ugeholl gëtt. Et gëtt dem Apparat Zäit fir de Wakreg-Signal ze verschaffen.

- **Bluetooth Scan Duration (Bluetooth Scan Dauer):** D'Dauer (a Sekonnen) wou d'Integratioun no Bluetooth Geräter scannt ier se probéiert de Paart Kommando ze schécken. E méi laange Scan kann hëllefen Geräter ze fannen déi lues sinn hir Präsenz ze annoncéieren.

## Liest an Ärer eegener Sprooch

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