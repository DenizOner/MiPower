# MiPower — Home Assistant pielāgota integrācija

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** ir Home Assistant integrācija, kas ļauj kontrolēt multivides atskaņotāju, kas neatbalsta tradicionālo Wake-on-LAN (WOL), bet kurus var "pamodināt" ar Bluetooth savienošanas pieprasījumu, strāvas stāvokli. Tā tika īpaši izstrādāta tādām ierīcēm kā Xiaomi Mi Box, taču tā var darboties arī ar citām līdzīgām Android TV kastēm.

Šī integrācija izveido `switch` (slēdža) entītiju Home Assistant. 
- Slēdža **ieslēgšana** nosūta Bluetooth komandu sēriju, izmantojot `bluetoothctl`, lai pamodinātu ierīci.
- Slēdža **izslēgšana** izsauc `media_player.turn_off` pakalpojumu piesaistītajai ierīcei.
- Slēdža stāvoklis tiek automātiski sinhronizēts ar piesaistītā multivides atskaņotāja entītijas stāvokli.

## 🤝 Atbalstiet

MiPower projekts tiek izstrādāts ar vīziju pievienot vērtību atvērtā koda kopienai. Jūsu atbalsts ir vitāli svarīgs, lai saglabātu šī projekta nepārtrauktību un attīstības ātrumu.

Ja novērtējat manu darbu, varat mani atbalstīt, izmantojot GitHub Sponsors vai šādas platformas. Paldies jau iepriekš!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Alternatīvi, jūs varat redzēt visas finansēšanas iespējas, noklikšķinot uz **Sponsora pogas (❤️)** repozitorija augšējā labajā stūrī.

## Priekšnosacījumi

- **Home Assistant OS / Supervised / Container:** Šai integrācijai ir nepieciešama uz Linux balstīta Home Assistant instalācija, kurā `bluetoothctl` komandrindas rīks ir pieejams un sasniedzams. Tā **nedarbosies** Home Assistant Core instalācijā operētājsistēmā Windows.

## Instalēšana, izmantojot HACS (ieteicams)

Šī integrācija ir pieejama kā pielāgots repozitorijs HACS.

1.  Pārejiet uz savu HACS vadības paneli.
2.  Noklikšķiniet uz **Integrations** (Integrācijas).
3.  Noklikšķiniet uz trīs punktu izvēlnes augšējā labajā stūrī un atlasiet **"Custom repositories"** ("Pielāgoti repozitoriji").
4.  Dialoglodziņā ievadiet šādu informāciju:
    - **Repository (Repozitorijs):** `https://github.com/DenizOner/MiPower`
    - **Category (Kategorija):** `Integration` (Integrācija)
5.  Noklikšķiniet **"Add"** ("Pievienot").
6.  "MiPower" integrācija tagad parādīsies jūsu HACS sarakstā. Noklikšķiniet uz tās.
7.  Noklikšķiniet uz pogas **"Download"** ("Lejupielādēt") un pēc tam nākamajā logā vēlreiz noklikšķiniet uz **"Download"** ("Lejupielādēt").
8.  Pēc lejupielādes pabeigšanas **jums ir jārestartē Home Assistant**, lai integrācija ielādētos.

## Manuāla instalēšana

Lai gan HACS ir ieteicamā metode, integrāciju var instalēt arī manuāli.

1.  Dodieties uz repozitorija [izlaidumu lapu](https://github.com/DenizOner/MiPower/releases) un lejupielādējiet failu `mipower.zip` no jaunākā izlaiduma.
2.  Atarhivējiet lejupielādēto failu.
3.  Atarhivētajā mapē atradīsit `custom_components` direktoriju. Kopējiet `mipower` mapi no tā.
4.  Ielīmējiet nokopēto `mipower` mapi `custom_components` mapē Home Assistant konfigurācijas direktorijā. Ja `custom_components` mape neeksistē, jums tā ir jāizveido.
    - Galīgajam ceļam jāizskatās šādi: `.../config/custom_components/mipower/`
5.  Restartējiet Home Assistant.

## Konfigurācija

Pēc restartēšanas jūs varat pievienot un konfigurēt MiPower slēdzi.

1.  Dodieties uz **Settings > Devices & Services** (Iestatījumi > Ierīces un Pakalpojumi).
2.  Noklikšķiniet uz pogas **"+ Add Integration"** ("+ Pievienot Integrāciju") apakšējā labajā stūrī.
3.  Meklējiet **"MiPower"** un noklikšķiniet uz tā.

### Vienkārša iestatīšana (ieteicams)

Šis ir vienkāršākais veids, kā konfigurēt integrāciju.

1.  Kad tiek prasīts, izvēlieties **"Easy Setup"** ("Vienkārša iestatīšana").
2.  Integrācija automātiski atklās Bluetooth iespējotos multivides atskaņotājus jūsu sistēmā.
3.  Nolaižamajā sarakstā atlasiet savu mērķa ierīci (piemēram, "Xiaomi Mi Box 4").
4.  Noklikšķiniet **"Submit"** ("Iesniegt").

Tas ir viss! Integrācija izveidos slēdzi, kas piesaistīts jūsu multivides atskaņotājam.

### Izvērstā iestatīšana

Izmantojiet šo metodi, ja Vienkāršā iestatīšana neatrod jūsu ierīci vai ja jums ir nepieciešams konfigurēt izvērstus laika iestatījumus jau no paša sākuma.

1.  **1. darbība: Ierīces izvēle**
    - Izvēlieties **"Advanced Setup"** ("Izvērstā iestatīšana").
    - Atlasiet savu mērķa multivides atskaņotāju no *visu* multivides atskaņotāju saraksta Home Assistant.
2.  **2. darbība: MAC adrese**
    - Integrācija mēģinās atrast izvēlētās ierīces Bluetooth MAC adresi. 
    - Ja tā tiek atrasta, tā tiks iepriekš aizpildīta. Pārbaudiet, vai tā ir pareiza.
    - Ja tā netiek atrasta, jums manuāli jāievada ierīces Bluetooth MAC adrese.
3.  **3. darbība: Laika iestatījumi**
    - Jūs varat konfigurēt dažādus taimautus un aizkaves Bluetooth komandām. Lielākajai daļai lietotāju ar noklusējuma vērtībām pietiks.
4.  Noklikšķiniet **"Submit"** ("Iesniegt"), lai pabeigtu iestatīšanu.

## Iespējas

Pēc MiPower slēdža konfigurēšanas jūs jebkurā laikā varat pielāgot laika iestatījumus.

1.  Dodieties uz **Settings > Devices & Services** (Iestatījumi > Ierīces un Pakalpojumi).
2.  Atrodiet MiPower integrāciju un noklikšķiniet **"Configure"** ("Konfigurēt").
3.  Pielāgojiet slīdņus *debounce*, taimautiem un aizkavēm pēc nepieciešamības.

## Laika iestatījumu skaidrojums

Konfigurācijas vai opciju izvēlnē varat precīzi noregulēt Bluetooth komandu laiku. Lielākajai daļai lietotāju noklusējuma vērtības darbojas labi.

- **Turn-On Debounce (Ieslēgšanas atcelšana):** Minimālais laiks (sekundēs), kuram jāpaiet, pirms komandu "ieslēgt" var izpildīt atkārtoti. Tas novērš ierīces bombardēšanu ar pamodināšanas signāliem, ja slēdzis tiek ātri pārslēgts.

- **Turn-Off Debounce (Izslēgšanas atcelšana):** Minimālais laiks (sekundēs), kuram jāpaiet, pirms komandu "izslēgt" var izpildīt atkārtoti. 

- **Delay Between Commands (Aizkave starp komandām):** Ļoti īsa aizkave (sekundēs) starp secīgu komandu nosūtīšanu `bluetoothctl` utilītai. Dažās sistēmās nelielas pauzes pievienošana var uzlabot uzticamību.

- **Process Spawn Timeout (Procesa starta taimauts):** Maksimālais laiks (sekundēs), lai gaidītu `bluetoothctl` procesa sākumu. Ja tas neizdosies sākties šajā laikā, ieslēgšanas mēģinājums neizdosies.

- **Pairing Timeout (Savienošanas taimauts):** Vienkāršotajā ieslēgšanas loģikā tas ir laiks, kas jāgaida pēc komandas `pair` nosūtīšanas, pirms tiek pieņemts, ka tas ir veiksmīgs. Tas dod ierīcei laiku apstrādāt pamodināšanas signālu.

- **Bluetooth Scan Duration (Bluetooth skenēšanas ilgums):** Ilgums (sekundēs), cik ilgi integrācija skenēs Bluetooth ierīces, pirms mēģinās nosūtīt savienošanas komandu. Garāka skenēšana var palīdzēt atrast ierīces, kuras lēni reklamē savu klātbūtni.

## Lasiet savā valodā

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