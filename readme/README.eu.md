# MiPower — Home Assistant-eko integrazio pertsonalizatua

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** Home Assistant-eko integrazio bat da, eta aukera ematen dizu Wake-on-LAN (WOL) tradizionala onartzen ez duten, baina Bluetooth parekatze-eskaera baten bidez "esnatu" daitezkeen multimedia-erreproduzitzaileen energia-egoera kontrolatzeko. Bereziki Xiaomi Mi Box bezalako gailuetarako diseinatu zen, baina antzeko beste Android TV box batzuekin ere funtziona dezake.

Integrazio honek `switch` (etengailu) entitate bat sortzen du Home Assistant-en. 
- Etengailua **PIZTUTA** jartzeak Bluetooth komando sorta bat bidaltzen du `bluetoothctl` bidez gailua esnatzeko.
- Etengailua **ITZALITA** jartzeak `media_player.turn_off` zerbitzua deitzen du lotutako gailurako.
- Etengailuaren egoera automatikoki sinkronizatzen da lotutako multimedia-erreproduzitzailearen entitatearen egoerarekin.

## 🤝 Lagundu

MiPower proiektua iturburu irekiko komunitateari balioa gehitzeko ikuspegiarekin garatzen ari da. Zure laguntza ezinbestekoa da proiektu honen jarraipena eta garapen-erritmoa mantentzeko.

Nire lana estimatzen baduzu, GitHub Sponsors edo ondorengo plataformen bidez lagundu ahal didazu. Eskerrik asko aldez aurretik!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Bestela, finantzaketa aukera guztiak ikus ditzakezu biltegiaren goiko eskuineko izkinan dagoen **Babesle botoian (❤️)** klik eginez.

## Aurrebaldintzak

- **Home Assistant OS / Supervised / Container:** Integrazio honek Linux-en oinarritutako Home Assistant instalazio bat behar du, non `bluetoothctl` komando-lerroko tresna eskuragarri eta irisgarri dagoen. **Ez** du funtzionatuko Windows-eko Home Assistant Core instalazio batean.

## Instalazioa HACS bidez (Gomendatua)

Integrazio hau HACS-en eskuragarri dago biltegi pertsonalizatu gisa.

1.  Joan zure HACS aginte-panelera.
2.  Egin klik **Integrations** (Integrazioak) aukeran.
3.  Egin klik goiko eskuineko izkinan dagoen hiru puntuko menuan eta hautatu **"Custom repositories"** ("Biltegi pertsonalizatuak").
4.  Elkarrizketa-koadroan, sartu informazio hau:
    - **Repository (Biltegia):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategoria):** `Integration` (Integrazioa)
5.  Egin klik **"Add"** ("Gehitu") botoian.
6.  "MiPower" integrazioa zure HACS zerrendan agertuko da orain. Egin klik gainean.
7.  Egin klik **"Download"** ("Deskargatu") botoian eta gero berriro **"Download"** ("Deskargatu") hurrengo leihoan.
8.  Deskarga amaitu ondoren, **Home Assistant berrabiarazi behar duzu** integrazioa kargatu ahal izateko.

## Eskuzko Instalazioa

HACS metodo gomendagarria den arren, integrazioa eskuz ere instalatu dezakezu.

1.  Joan biltegiaren [Bertsio orrira](https://github.com/DenizOner/MiPower/releases) eta deskargatu azken bertsioaren `mipower.zip` fitxategia.
2.  Deskonprimitu deskargatutako fitxategia.
3.  Deskonprimitutako karpetaren barruan, `custom_components` direktorio bat aurkituko duzu. Kopiatu bertatik `mipower` karpeta.
4.  Itsatsi kopiatutako `mipower` karpeta zure Home Assistant konfigurazio-direktorioko `custom_components` karpetan. `custom_components` karpeta existitzen ez bada, sortu egin behar duzu.
    - Azken bideak honelakoa izan beharko luke: `.../config/custom_components/mipower/`
5.  Berrabiarazi Home Assistant.

## Konfigurazioa

Berrabiarazi ondoren, MiPower etengailua gehitu eta konfigura dezakezu.

1.  Joan **Settings > Devices & Services** (Ezarpenak > Gailuak eta Zerbitzuak) atalera.
2.  Egin klik **"+ Add Integration"** ("+ Gehitu integrazioa") botoian beheko eskuineko izkinan.
3.  Bilatu **"MiPower"** eta egin klik gainean.

### Konfigurazio Erraza (Gomendatua)

Hau da integrazioa konfiguratzeko modurik errazena.

1.  Eskatzen zaizunean, aukeratu **"Easy Setup"** ("Konfigurazio erraza").
2.  Integrazioak automatikoki ezagutuko ditu zure sistemako Bluetooth bidezko multimedia-erreproduzitzaileak.
3.  Aukeratu zure helburuko gailua (adibidez, "Xiaomi Mi Box 4") goitibeherako zerrendan.
4.  Egin klik **"Submit"** ("Bidali").

Hori da dena! Integrazioak zure multimedia-erreproduzitzailearekin lotutako etengailu bat sortuko du.

### Konfigurazio Aurreratua

Erabili metodo hau Konfigurazio Errazak zure gailua aurkitzen ez badu edo hasieratik denbora-ezarpen aurreratuak konfiguratu behar badituzu.

1.  **1. urratsa: Gailuaren Hautaketa**
    - Aukeratu **"Advanced Setup"** ("Konfigurazio aurreratua").
    - Hautatu zure helburuko multimedia-erreproduzitzailea zure Home Assistant-eko *multimedia-erreproduzitzaile guztien* zerrendatik.
2.  **2. urratsa: MAC Helbidea**
    - Integrazioak hautatutako gailuaren Bluetooth MAC helbidea aurkitzen saiatuko da. 
    - Aurkitzen bada, aurrez beteta egongo da. Egiaztatu zuzena dela.
    - Aurkitzen ez bada, zure gailuaren Bluetooth MAC helbidea eskuz sartu behar duzu.
3.  **3. urratsa: Denbora Ezarpenak**
    - Bluetooth komandoetarako hainbat denbora-muga eta atzerapen konfigura ditzakezu. Erabiltzaile gehienentzat, balio lehenetsiak nahikoak dira.
4.  Egin klik **"Submit"** ("Bidali") konfigurazioa osatzeko.

## Aukerak

MiPower etengailua konfiguratu ondoren, denbora-ezarpenak edonoiz egokitu ditzakezu.

1.  Joan **Settings > Devices & Services** (Ezarpenak > Gailuak eta Zerbitzuak) atalera.
2.  Bilatu MiPower integrazioa eta egin klik **"Configure"** ("Konfiguratu") botoian.
3.  Egokitu *debounce*, denbora-mugak eta atzerapenak behar den moduan.

## Denbora Ezarpenen Azalpena

Konfigurazio edo aukeren menuan, Bluetooth komandoen denbora zehatz-mehatz doitu dezakezu. Erabiltzaile gehienentzat, balio lehenetsiek ondo funtzionatzen dute.

- **Turn-On Debounce (Pizteko Debounce):** 'Piztu' komandoa berriro exekutatu aurretik igaro behar den gutxieneko denbora (segundotan). Honek gailua esnatze-seinalez ez betetzea eragozten du etengailua azkar aldatzen bada.

- **Turn-Off Debounce (Itzaltzeko Debounce):** 'Itzali' komandoa berriro exekutatu aurretik igaro behar den gutxieneko denbora (segundotan). 

- **Delay Between Commands (Atzerapena Komandoen Artean):** Oso atzerapen laburra (segundotan) ondoz ondoko komandoak `bluetoothctl` utilitateari bidaltzearen artean. Sistema batzuetan, etenaldi txiki bat gehitzeak fidagarritasuna hobetu dezake.

- **Process Spawn Timeout (Prozesua Sortzeko Denbora-muga):** `bluetoothctl` prozesua hasteko itxaron behar den gehieneko denbora (segundotan). Denbora horretan hasten ez bada, pizteko saiakerak huts egingo du.

- **Pairing Timeout (Parekatze Denbora-muga):** Pizteko logika sinplifikatuan, hau da `pair` komandoa bidali ondoren arrakasta suposatu aurretik itxaron beharreko denbora. Gailuari esnatze-seinalea prozesatzeko denbora ematen dio.

- **Bluetooth Scan Duration (Bluetooth Eskaneatzearen Iraupena):** Integrazioak Bluetooth gailuak eskaneatzeko iraunaldia (segundotan), parekatze-komandoa bidali aurretik. Eskaneatze luzeago batek bere presentzia iragartzen motelak diren gailuak aurkitzen lagun dezake.

## Irakurri zure hizkuntzan

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