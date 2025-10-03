# MiPower — Kevytthelvaans dhyworth Home Assistant

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** yw kevytthaelvaans Home Assistant a wra gasa dhis rewlya studh nerth gwarioryon media nag yns i ow skoodhya Wake-on-LAN (WOL) koth, mes a yll bos "dihunys" gans govyn parow Bluetooth. Ev a veu designys yn arbennik rag daffar kepar ha Xiaomi Mi Box, mes ev a yll oberi gans boksys Android TV hevelep erel.

An gevytthaelvaans ma a wra kroui entita `switch` (channjyer) yn Home Assistant. 
- **Trei war** an channjyer a dhannvon kevres a worhemmynnow Bluetooth dre `bluetoothctl` rag dihun an daffar.
- **Trei dhe-ves** an channjyer a yll an servisyans `media_player.turn_off` rag an daffar kevys.
- Studh an channjyer a rewl awtomatek gans studh entita an gwarior media kevys.

## 🤝 Skoodhyewgh

Towljyans MiPower yw displegyes gans visyon dhe yeghes talvosigeth dhe'n gemeneth open source. Aga skoodhyans yw pur bosek rag gwitha an gontinyuityans ha speed a dhisplegyans an towljyans ma.

Mar kwrewgh kymmeres ow oboedhes, hy kowgh skoodhya dre GitHub Sponsors po an plateformow a sew. Meur ras a-gynsow!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Avel dewis arall, y hyllowgh gweles oll an etholans finansya dre gleckya war an **Boten Skoodhyer (❤️)** y'n korn ughel a-dheghow a'n gwithva.

## Kynskisyow

- **Home Assistant OS / Supervised / Container:** An gevytthaelvaans ma a grys installaans Home Assistant selys war Linux le mayth yw an toulys linen-gorhemmyn `bluetoothctl` kavadow ha kerdadow. Ev **ny** wra oberi war installaans Home Assistant Core war Windows.

## Installans dre HACS (Gwarnys)

An gevytthaelvaans ma yw kavadow avel repositori kevys yn HACS.

1.  Kerdh dhe'th Daslegh HACS.
2.  Klycky war **Integrations** (Kevytthaelvansow).
3.  Klycky war an valva tri-boen y'n kornel a-wartha a-dhyghow ha dewis **"Custom repositories"** ("Repositirisow kevys").
4.  Yn kist an dyanter, entray an kedhlow ma:
    - **Repository (Repositori):** `https://github.com/DenizOner/MiPower`
    - **Category (Klass):** `Integration` (Kevytthaelvaans)
5.  Klycky **"Add"** ("Kevyttha").
6.  An kevytthaelvaans "MiPower" a wra dos war an rol HACS lemmyn. Klycky warnodho.
7.  Klycky an boen **"Download"** ("Isel-karga") ha wosa klycky **"Download"** ("Isel-karga") arta y'n fenester nessa.
8.  Wosa an isel-karga bos kowlwrys, **res yw dhis dhe dhalleth Home Assistant arta** rag an kevytthaelvaans dhe garga.

## Installans Dhornweyth

Kyn feu HACS an arwodh gwarnys, ty a yll installa an kevytthaelvaans dhornweyth ynwedh.

1.  Ke dhe [folen Dyllansow](https://github.com/DenizOner/MiPower/releases) an repositori ha isel-karga an restr `mipower.zip` dhyworth an dyllans diwettha.
2.  Digompress an restr isel-kargys.
3.  Yn-mysk an fowlen digompressys, ty a wyl dyrektor `custom_components`. Kopii an fowlen `mipower` dhyworti.
4.  Past an fowlen `mipower` kopisys y'n fowlen `custom_components` yn dyrektor fowlenwa an Home Assistant. Mars nag yw an fowlen `custom_components` kavadow, res yw dhis hy kroui.
    - An hyns diwettha a dal dh'y hevelebi: `.../config/custom_components/mipower/`
5.  Dalleth Home Assistant arta.

## Fowlenwa

Wosa an dhalleth arta, ty a yll kevyttha ha fowlenwi an channjyer MiPower.

1.  Ke dhe **Settings > Devices & Services** (Settyansow > Daffar ha Servisyow).
2.  Klycky an boen **"+ Add Integration"** ("+ Kevyttha Kevytthaelvaans") y'n kornel a-wartha a-dhyghow.
3.  Hwila rag **"MiPower"** ha klycky warnodho.

### Settyans Esel (Gwarnys)

Hemm yw an fordh esella rag fowlenwi an kevytthaelvaans.

1.  Pan veu govynnys, dewis **"Easy Setup"** ("Settyans Esel").
2.  An kevytthaelvaans a wra diskudha awtomatek gwarioryon media Bluetooth-gerthel war dy system.
3.  Dewis an daffar mir-dy (r.e., "Xiaomi Mi Box 4") dhyworth an rol-dov.
4.  Klycky **"Submit"** ("Danvon").

Hemm yw! An kevytthaelvaans a wra kroui channjyer kevys dhe ty warior media.

### Settyans Avonsys

Devnydh an arwodh ma mars nag yw Settyans Esel ow kavos ty daffar po mars eus ty res dhe fowlenwi settyansow dermyn avonsys dhyworth an dalleth.

1.  **Kamm 1: Dewis Daffar**
    - Dewis **"Advanced Setup"** ("Settyans Avonsys").
    - Dewis ty warior media mir-dy dhyworth an rol a *oll* an warioryon media y'th Home Assistant.
2.  **Kamm 2: MAC Adres**
    - An kevytthaelvaans a wra assaya dhe gavos MAC Adres Bluetooth an daffar dewisys. 
    - Mars yw kavys, ev a vydh kyns-leunys. Gweler mars yw ev ewn.
    - Mars yw nag yw kavys, res yw dhis entray MAC Adres Bluetooth ty daffar dhornweyth.
3.  **Kamm 3: Settyansow Dermyn**
    - Ty a yll fowlenwi dermynnow-diwedh ha deleyansow dyffrans rag an gorhemmynnow Bluetooth. Rag an brassa rann a'n dornwedhyoryon, an talvosow dre-veth yw lowr.
4.  Klycky **"Submit"** ("Danvon") rag kowlwul an settyans.

## Dewisyansow

Wosa ty dhe fowlenwi ty channjyer MiPower, ty a yll rewl settyansow dermyn y'n prys a vydh.

1.  Ke dhe **Settings > Devices & Services** (Settyansow > Daffar ha Servisyow).
2.  Kav an kevytthaelvaans MiPower ha klycky **"Configure"** ("Fowlenwi").
3.  Rewl an resegoryon rag *debounce*, dermynnow-diwedh, ha deleyansow kepar ha res.

## Esplegyans Settyansow Dermyn

Yn valva fowlenwa po dewisyansow, ty a yll rewl dermyn an gorhemmynnow Bluetooth yn manylys. Rag an brassa rann a'n dornwedhyoryon, an talvosow dre-veth a ober yn ta.

- **Turn-On Debounce (Debounce Drei War):** An dermyn leun (yn sekundys) a dal dh'y bassya kyns an gorhemmyn 'trei war' a yll bos ekskusys arta. Hemm a wra difres spammy an daffar gans arwodhnow dihun mars yw an channjyer gwrys yn uskis.

- **Turn-Off Debounce (Debounce Drei Dhe-ves):** An dermyn leun (yn sekundys) a dal dh'y bassya kyns an gorhemmyn 'trei dhe-ves' a yll bos ekskusys arta. 

- **Delay Between Commands (Deleyans Yn-mysk Gorhemmynnow):** Deleyans pur verr (yn sekundys) yn-mysk danvon gorhemmynnow hevel dhe `bluetoothctl` toulys. War re systemys, kevyttha saw leun a yll gwellhe rewlyans.

- **Process Spawn Timeout (Dermyn-Diwedh Geni Provas):** An dermyn gwartha (yn sekundys) rag gortos rag an `bluetoothctl` provas dhe dhalleth. Mars yw ev ow fyllel dh'y dhalleth y'n dermyn ma, an assaya trei war a wra fyllel.

- **Pairing Timeout (Dermyn-Diwedh Parow):** Yn logek drei war esel, hemm yw an dermyn a dal dh'y gortos wosa danvon an gorhemmyn `pair` kyns an govennek a sowena. Ev a re dermyn dhe'n daffar rag proessa an arwodh dihun.

- **Bluetooth Scan Duration (Hys Skannyans Bluetooth):** An hys (yn sekundys) a wra an kevytthaelvaans skannya rag daffar Bluetooth kyns assaya dhe dhannvon an gorhemmyn parow. Skannyans hirra a yll gweres kavos daffar a vydh ow sevel dhe wolowes aga bos kavadow.

## Redyewgh yn agas yeth

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