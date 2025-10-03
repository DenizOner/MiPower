# MiPower — Benutzerdefinierti Home Assistant Integration

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** isch ä Home Assistant Integration, wo's Dir erlaubt, dä Stromstatus vo Media Player z'stüüre, wo s'traditionelli Wake-on-LAN (WOL) nöd unterstützed, aber dur ä Bluetooth-Kopplungsafrag "ufgweckt" wärde chönd. S'isch speziell für Grät wie d'Xiaomi Mi Box entworfe worde, chann aber au mit andere ähnliche Android TV-Boxe funktioniere.

Die Integration erstellt ä `switch`-Entität (Schalter) i Home Assistant. 
- **Iischalte** vom Schalter schickt ä Serie vo Bluetooth-Befähl über `bluetoothctl`, um s'Grät ufz'wecke.
- **Usschalte** vom Schalter rüeft dä Dienscht `media_player.turn_off` für s'verknüpfti Grät uf.
- De Status vom Schalter wird automatisch mit em Status vo dä verknüpftä Media Player-Entität synchronisiert.

## 🤝 Unterstützen Sie uns

Das MiPower-Projekt wird mit der Vision entwickelt, der Open-Source-Community einen Mehrwert zu bieten. Ihre Unterstützung ist entscheidend, um die Kontinuität und Entwicklungsgeschwindigkeit dieses Projekts aufrechtzuerhalten.

Wenn Sie meine Arbeit schätzen, können Sie mich über GitHub Sponsors oder die folgenden Plattformen unterstützen. Vielen Dank im Voraus!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternativ können Sie alle Finanzierungsmöglichkeiten sehen, indem Sie auf den **Sponsor-Button (❤️)** in der oberen rechten Ecke des Repositorys klicken.

## Voruussetzige

- **Home Assistant OS / Supervised / Container:** Die Integration brucht ä Linux-basierti Home Assistant Installation, bi dä's Kommandoziile-Tool `bluetoothctl` verfügbar und zuegänglich isch. S'wird **nöd** ufere Home Assistant Core Installation uf Windows funktioniere.

## Installation über HACS (Empfohle)

Die Integration isch als benutzerdefinierts Repository i HACS verfügbar.

1.  Navigier zu Dim HACS-Dashboard.
2.  Klick uf **Integrations** (Integratioone).
3.  Klick uf s'Drei-Pünkt-Menü i dä obe rächte Ecke und wähl **"Custom repositories"** ("Benutzerdefinierti Repositories").
4.  Gib im Dialogfeld diä folgendi Information ii:
    - **Repository:** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorii):** `Integration` (Integration)
5.  Klick uf **"Add"** ("Hinzüefüegä").
6.  D' "MiPower"-Integration wird jetzt i Diner HACS-Lischte azeigt. Klick druf.
7.  Klick uf dä Knopf **"Download"** ("Abeladä") und dänn no mal uf **"Download"** ("Abeladä") im nöchschte Fänschter.
8.  Nachem Abschlüess vom Abeladä **muesch Du Home Assistant neu startä**, damit d'Integration glade wärde chann.

## Manuell Installatioon

Obwohl HACS diä empfohli Methode isch, chasch Du d'Integration au manuell installierä.

1.  Gah uf d' [Releases-Siite](https://github.com/DenizOner/MiPower/releases) vom Repository und lad de `mipower.zip`-Datei vo dä nöchschte Versioon ab.
2.  Entpack diä abegladeni Datei.
3.  Innerhalb vom entpacktä Ordner findsch ä Verzeichnis namens `custom_components`. Kopier de Ordner `mipower` duss.
4.  Füeg de kopierti Ordner `mipower` in de Ordner `custom_components` i Dim Home Assistant Konfigurationsverzeichnis ii. Falls dä Ordner `custom_components` nöd existiert, muesch ihn erstellä.
    - Dä endgültig Pfad söll so usgseh: `.../config/custom_components/mipower/`
5.  Start Home Assistant neu.

## Konfiguraatioon

Nachem Neustart chasch de MiPower-Schalter hiezüefüegä und konfigurierä.

1.  Gah zue **Settings > Devices & Services** (Iistellige > Grät & Dienscht).
2.  Klick uf dä Knopf **"+ Add Integration"** ("+ Integration hiezüefüegä") i dä untere rächte Ecke.
3.  Suech nach **"MiPower"** und klick druf.

### Einfachi Iirichtig (Empfohle)

Das isch dä eifachscht Wäg, um d'Integration z'konfigurierä.

1.  Wenn Du ufgforderet wirsch, wähl **"Easy Setup"** ("Eifachi Iirichtig").
2.  D'Integration findt automatisch Bluetooth-fähigi Media Player uf Dim System.
3.  Wähl Diis Zielgrät (z.B. "Xiaomi Mi Box 4") us dä Dropdown-Lischte.
4.  Klick uf **"Submit"** ("Abeschickä").

Das isch es! D'Integration erstellt ä Schalter, wo mit Dim Media Player verchnüpft isch.

### Erwiitereti Iirichtig

Bruuch die Methode, wenn d'eifachi Iirichtig Diis Grät nöd findt oder wenn Du erwiitereti Timing-Iistellige vo Afang a muesch konfigurierä.

1.  **Schritt 1: Grätuuswahl**
    - Wähl **"Advanced Setup"** ("Erwiitereti Iirichtig").
    - Wähl Diis Ziel-Media Player us dä Lischte vo *allne* Media Player i Dim Home Assistant.
2.  **Schritt 2: MAC-Adräss**
    - D'Integration versucht, d'Bluetooth MAC-Adräss vom usgwähltä Grät z'findä. 
    - Wenn sie gfunde wird, wird sie vorusgfüült. Verifizier, dass si korrekt isch.
    - Wenn si nöd gfunde wird, muesch d'Bluetooth MAC-Adräss vo Dim Grät manuell iigäh.
3.  **Schritt 3: Timing-Iistellige**
    - Du chasch verschideni Timeouts und Verzögerige für d'Bluetooth-Befähl konfigurierä. Für diä meischte Benutzer sind d'Standardwärt gnueg.
4.  Klick uf **"Submit"** ("Abeschickä"), um d'Iirichtig abz'schlüssä.

## Optioone

Wenn Du Di MiPower-Schalter konfiguriert hesch, chasch d'Timing-Iistellige jederzeit aapassä.

1.  Gah zue **Settings > Devices & Services** (Iistellige > Grät & Dienscht).
2.  Suech d'MiPower-Integration und klick uf **"Configure"** ("Konfigurierä").
3.  Pass d'Schieberegler für Debouncing, Timeouts und Verzögerige nach Bedarfs a.

## Erchlärig vo dä Timing-Iistellige

Im Konfigurations- oder Optionsmenü chasch s'Timing vo dä Bluetooth-Befähl fyniaastellä. Für diä meischte Benutzer funktioniere d'Standardwärt guet.

- **Turn-On Debounce (Iischalt-Entprellig):** Diä minimal Ziit (i Sekunde), wo vergah mues, bevor de 'Iischalt'-Befähl wider usgfüehrt wärde chann. Das verhindert, dass s'Grät mit Ufwecksignal überflüetet wird, wenn de Schalter schnäll umg'schalted wird.

- **Turn-Off Debounce (Usschalt-Entprellig):** Diä minimal Ziit (i Sekunde), wo vergah mues, bevor de 'Usschalt'-Befähl wider usgfüehrt wärde chann. 

- **Delay Between Commands (Verzögerig zwüsche de Befähl):** Ä sehr chliini Verzögerig (i Sekunde) zwüschem Schickä vo nooeinanderfolgende Befähl an s' `bluetoothctl`-Dienstprogramm. Uf gwüsse Systeme chann s'Hiezüefüegä vo ere chliine Pausä d'Zueverlässigkeit verbessere.

- **Process Spawn Timeout (Ziitüberschriitig bim Prozessstart):** Diä maximal Ziit (i Sekunde), wo uf dä Start vom `bluetoothctl`-Prozess gwartet wird. Falls de Start innert däre Ziit fehlschlaat, schlaat de Iischaltversuech au feh.

- **Pairing Timeout (Ziitüberschriitig bim Kopplä):** I dä vereifachtä Iischaltlogik isch das d'Ziit, wo nach em Schickä vom `pair`-Befähl gwartet wird, bevors Erfolg aagnoh wird. S'git em Grät Ziit, s'Ufwecksignal z'verarbeitä.

- **Bluetooth Scan Duration (Dueri vom Bluetooth-Scan):** D'Dueri (i Sekunde), für diä d'Integration nach Bluetooth-Grät suecht, bevor Versuecht wird, de Kopplungsbefähl z'schickä. Ä längere Scan chann helfä, Grät z'findä, wo ihri Aawäsenheit nume langsam aachündäged.

## Lesen Sie in Ihrer Sprache

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