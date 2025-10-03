# MiPower — Home Assistanti kohandatud integratsioon

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** on Home Assistanti integratsioon, mis võimaldab sul juhtida meediapleierite toiteolekut, mis ei toeta traditsioonilist Wake-on-LAN (WOL), kuid mida saab "äratada" Bluetoothi sidumistaotlusega. See oli spetsiaalselt loodud seadmetele nagu Xiaomi Mi Box, kuid võib töötada ka teiste sarnaste Android TV-boksidega.

See integratsioon loob Home Assistantis `switch` (lüliti) olemi. 
- Lüliti **sisselülitamine** saadab seadme äratamiseks rea Bluetoothi käske `bluetoothctl` kaudu.
- Lüliti **väljalülitamine** kutsub seotud seadme jaoks välja teenuse `media_player.turn_off`.
- Lüliti olek sünkroonitakse automaatselt seotud meediapleieri olemi olekuga.

## 🤝 Toetage

MiPower projekt on arendatud visiooniga lisada väärtust avatud lähtekoodiga kogukonnale. Teie toetus on elutähtis selle projekti järjepidevuse ja arengutempo säilitamiseks.

Kui te hindate minu tööd, saate mind toetada GitHub Sponsors või järgmiste platvormide kaudu. Tänan juba ette!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatiivina saate näha kõiki rahastamisvõimalusi, klõpsates hoidla paremas ülanurgas asuval **Sponsori nupul (❤️)**.

## Eeltingimused

- **Home Assistant OS / Supervised / Container:** See integratsioon nõuab Linux-põhist Home Assistanti installatsiooni, kus `bluetoothctl` käsurea tööriist on saadaval ja ligipääsetav. See **ei** tööta Windowsi Home Assistant Core installatsioonis.

## Paigaldamine HACS-i kaudu (Soovitatav)

See integratsioon on HACS-is saadaval kohandatud repositooriumina.

1.  Navigeeri oma HACS-i juhtpaneelile.
2.  Klõpsa **Integrations** (Integratsioonid).
3.  Klõpsa paremas ülanurgas kolme punktiga menüüle ja vali **"Custom repositories"** ("Kohandatud repositooriumid").
4.  Sisesta dialoogikastis järgmine teave:
    - **Repository (Repositoorium):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategooria):** `Integration` (Integratsioon)
5.  Klõpsa **"Add"** ("Lisa").
6.  "MiPower" integratsioon ilmub nüüd sinu HACS-i nimekirja. Klõpsa sellel.
7.  Klõpsa nupul **"Download"** ("Laadi alla") ja seejärel klõpsa järgmises aknas uuesti **"Download"** ("Laadi alla").
8.  Pärast allalaadimise lõpetamist **pead sa Home Assistanti taaskäivitama**, et integratsioon saaks laadida.

## Käsitsi Paigaldamine

Kuigi HACS on soovitatav meetod, saad integratsiooni paigaldada ka käsitsi.

1.  Mine repositooriumi [Väljalasked lehele](https://github.com/DenizOner/MiPower/releases) ja laadi alla `mipower.zip` fail uusimast väljalaskest.
2.  Paki allalaaditud fail lahti.
3.  Lahtipakitud kausta sees leiad `custom_components` kataloogi. Kopeeri sealt `mipower` kaust.
4.  Kleebi kopeeritud `mipower` kaust oma Home Assistanti konfiguratsioonikataloogi `custom_components` kausta. Kui `custom_components` kausta ei eksisteeri, pead selle looma.
    - Lõplik tee peaks välja nägema selline: `.../config/custom_components/mipower/`
5.  Taaskäivita Home Assistant.

## Konfigureerimine

Pärast taaskäivitamist saad MiPower lüliti lisada ja konfigureerida.

1.  Mine **Settings > Devices & Services** (Seaded > Seadmed ja Teenused).
2.  Klõpsa paremas alanurgas nupule **"+ Add Integration"** ("+ Lisa integratsioon").
3.  Otsi **"MiPower"** ja klõpsa sellel.

### Lihtne Seadistus (Soovitatav)

See on kõige lihtsam viis integratsiooni konfigureerimiseks.

1.  Küsimisel vali **"Easy Setup"** ("Lihtne seadistus").
2.  Integratsioon avastab automaatselt sinu süsteemis Bluetoothiga varustatud meediapleierid.
3.  Vali rippmenüüst oma sihtseade (nt "Xiaomi Mi Box 4").
4.  Klõpsa **"Submit"** ("Esita").

See on kõik! Integratsioon loob sinu meediapleieriga seotud lüliti.

### Täpsem Seadistus

Kasuta seda meetodit, kui Lihtne Seadistus sinu seadet ei leia või kui sul on vaja kohe alguses konfigureerida täpsemaid ajastuse seadeid.

1.  **Samm 1: Seadme Valik**
    - Vali **"Advanced Setup"** ("Täpsem seadistus").
    - Vali oma sihtmeediapleier oma Home Assistanti *kõikide* meediapleierite nimekirjast.
2.  **Samm 2: MAC-aadress**
    - Integratsioon proovib leida valitud seadme Bluetoothi MAC-aadressi. 
    - Kui leitakse, täidetakse see eeltäidetuna. Kontrolli, et see oleks õige.
    - Kui ei leita, pead sa käsitsi sisestama oma seadme Bluetoothi MAC-aadressi.
3.  **Samm 3: Ajastuse Seaded**
    - Sa saad konfigureerida erinevaid ajalõppe ja viivitusi Bluetoothi käskude jaoks. Enamiku kasutajate jaoks piisab vaikeseadetest.
4.  Klõpsa seadistuse lõpetamiseks **"Submit"** ("Esita").

## Valikud

Pärast MiPower lüliti konfigureerimist saad ajastuse seadeid igal ajal muuta.

1.  Mine **Settings > Devices & Services** (Seaded > Seadmed ja Teenused).
2.  Leia MiPower integratsioon ja klõpsa **"Configure"** ("Konfigureeri").
3.  Reguleeri liugureid *debounce*’i, ajalõppude ja viivituste jaoks vastavalt vajadusele.

## Ajastuse Seadete Selgitus

Konfigureerimise või valikute menüüs saad Bluetoothi käskude ajastust peenhäälestada. Enamiku kasutajate jaoks töötavad vaikeseaded hästi.

- **Turn-On Debounce (Sisselülitamise Viide):** Minimaalne aeg (sekundites), mis peab mööduma enne, kui käsku 'lülita sisse' saab uuesti täita. See väldib seadme üleujutamist äratussignaalidega, kui lülitit kiiresti lülitatakse.

- **Turn-Off Debounce (Väljalülitamise Viide):** Minimaalne aeg (sekundites), mis peab mööduma enne, kui käsku 'lülita välja' saab uuesti täita. 

- **Delay Between Commands (Viivitus käskude vahel):** Väga lühike viivitus (sekundites) järjestikuste käskude saatmise vahel `bluetoothctl` utiliidile. Mõnedel süsteemidel võib lühikese pausi lisamine usaldusväärsust parandada.

- **Process Spawn Timeout (Protsessi Käivitamise Ajalõpp):** Maksimaalne aeg (sekundites), mil oodata `bluetoothctl` protsessi käivitumist. Kui see selle aja jooksul käivituda ei suuda, ebaõnnestub sisselülitamise katse.

- **Pairing Timeout (Sidumise Ajalõpp):** Lihtsustatud sisselülitamise loogikas on see aeg, mil oodatakse pärast `pair` käsu saatmist enne edukuse eeldamist. See annab seadmele aega äratussignaali töötlemiseks.

- **Bluetooth Scan Duration (Bluetoothi Skannimise Kestus):** Kestus (sekundites), mille jooksul integratsioon otsib Bluetoothi seadmeid enne sidumiskäsu saatmist. Pikem skannimine võib aidata leida seadmeid, mis oma olemasolust aeglaselt teatavad.

## Lugege oma keeles

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