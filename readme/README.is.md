# MiPower — Sérsniðin Home Assistant samþætting

[![HACS Custom Repo](https://img.shields.io/badge/HACS-Custom%20Repo-181717.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DenizOner&repository=MiPower&category=integration)
[![GitHub Release](https://img.shields.io/github/v/release/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/releases)
[![License](https://img.shields.io/github/license/DenizOner/MiPower?style=for-the-badge)](https://github.com/DenizOner/MiPower/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/DenizOner/MiPower?style=for-the-badge&logo=github)](https://github.com/DenizOner/MiPower/issues)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DenizOner?style=for-the-badge&logo=github&label=Sponsor)](https://github.com/sponsors/DenizOner)

--- 

**MiPower** er Home Assistant samþætting sem gerir þér kleift að stjórna aflstöðu margmiðlunarspilara sem styðja ekki hefðbundið Wake-on-LAN (WOL), en er hægt að "vekja" með Bluetooth pörunarbeiðni. Hún var sérstaklega hönnuð fyrir tæki eins og Xiaomi Mi Box, en gæti virkað með öðrum svipuðum Android TV boxum.

Þessi samþætting býr til `switch` (rofa) einingu í Home Assistant. 
- **Að kveikja** á rofanum sendir röð af Bluetooth skipunum í gegnum `bluetoothctl` til að vekja tækið.
- **Að slökkva** á rofanum kallar á `media_player.turn_off` þjónustuna fyrir tengda tækið.
- Staða rofans er sjálfkrafa samstillt við stöðu tengdu margmiðlunarspilarareiningarinnar.

## 🤝 Styðjið okkur

MiPower verkefnið er þróað með þá sýn að bæta virði við opinn hugbúnaðarsamfélagið. Stuðningur þinn er mikilvægur til að viðhalda samfellu og þróunarhraða þessa verkefnis.

Ef þú metur vinnu mína, geturðu stutt mig í gegnum GitHub Sponsors eða eftirfarandi vettvanga. Takk fyrirfram!

* [**GitHub Sponsors**](https://github.com/sponsors/DenizOner)
* [**Patreon**](https://patreon.com/rDenizOner)
* [**Buy Me a Coffee**](https://www.buymeacoffee.com/DenizOner)

Að öðrum kosti geturðu séð alla fjármögnunarmöguleika með því að smella á **Styrktarhnappinn (❤️)** í efra hægra horni geymslunnar.

## Forsendur

- **Home Assistant OS / Supervised / Container:** Þessi samþætting krefst Linux-undirstaða Home Assistant uppsetningar þar sem `bluetoothctl` skipanalínutólið er tiltækt og aðgengilegt. Hún mun **ekki** virka á Home Assistant Core uppsetningu á Windows.

## Uppsetning í gegnum HACS (Mælt með)

Þessi samþætting er fáanleg sem sérsniðið safn í HACS.

1.  Farðu á HACS mælaborðið þitt.
2.  Smelltu á **Integrations** (Samþættingar).
3.  Smelltu á þriggja punkta valmyndina í efra hægra horninu og veldu **"Custom repositories"** ("Sérsniðin söfn").
4.  Í glugganum, sláðu inn eftirfarandi upplýsingar:
    - **Repository (Safn):** `https://github.com/DenizOner/MiPower`
    - **Category (Flokkur):** `Integration` (Samþætting)
5.  Smelltu á **"Add"** ("Bæta við").
6.  "MiPower" samþættingin mun nú birtast á HACS listanum þínum. Smelltu á hana.
7.  Smelltu á **"Download"** ("Sækja") hnappinn og smelltu síðan aftur á **"Download"** ("Sækja") í næsta glugga.
8.  Eftir að niðurhal er lokið, **verður þú að endurræsa Home Assistant** til að samþættingin hlaðist.

## Handvirk uppsetning

Þó að HACS sé mælt með aðferðinni, getur þú líka sett samþættinguna upp handvirkt.

1.  Farðu á [Útgáfusíðu](https://github.com/DenizOner/MiPower/releases) safnsins og halaðu niður `mipower.zip` skránni úr nýjustu útgáfunni.
2.  Taktu niðurhalsskrána úr þjöppun.
3.  Inni í unpakkaðri möppu finnur þú `custom_components` möppu. Afritaðu `mipower` möppuna innan úr henni.
4.  Límdu afrituðu `mipower` möppuna inn í `custom_components` möppuna í stillingarskrá Home Assistant. Ef `custom_components` mappan er ekki til, verður þú að búa hana til.
    - Endanleg slóð ætti að líta svona út: `.../config/custom_components/mipower/`
5.  Endurræstu Home Assistant.

## Stillingar

Eftir endurræsingu getur þú bætt við og stillt MiPower rofann.

1.  Farðu í **Settings > Devices & Services** (Stillingar > Tæki og þjónustur).
2.  Smelltu á **"+ Add Integration"** ("+ Bæta við samþættingu") hnappinn í neðra hægra horninu.
3.  Leitaðu að **"MiPower"** og smelltu á það.

### Auðveld Stilling (Mælt með)

Þetta er einfaldasta leiðin til að stilla samþættinguna.

1.  Þegar beðið er um það, veldu **"Easy Setup"** ("Auðveld stilling").
2.  Samþættingin mun sjálfkrafa finna Bluetooth-virkjaða margmiðlunarspilara á kerfinu þínu.
3.  Veldu markmiðstækið þitt (t.d. "Xiaomi Mi Box 4") úr fellilistanum.
4.  Smelltu á **"Submit"** ("Senda").

Það er allt! Samþættingin mun búa til rofa sem er tengdur við margmiðlunarspilarann þinn.

### Ítarleg Stilling

Notaðu þessa aðferð ef Auðveld Stilling finnur ekki tækið þitt eða ef þú þarft að stilla ítarlegar tímasetningarstillingar frá upphafi.

1.  **Skref 1: Val á tæki**
    - Veldu **"Advanced Setup"** ("Ítarleg stilling").
    - Veldu markmiðs margmiðlunarspilara úr lista yfir *alla* margmiðlunarspilara í Home Assistant.
2.  **Skref 2: MAC vistfang**
    - Samþættingin mun reyna að finna Bluetooth MAC vistfang valda tækisins. 
    - Ef það finnst, verður það fyrirfram útfyllt. Staðfestu að það sé rétt.
    - Ef það finnst ekki, verður þú að slá inn Bluetooth MAC vistfang tækisins handvirkt.
3.  **Skref 3: Tímasetningarstillingar**
    - Þú getur stillt ýmsar tímamörk og tafir fyrir Bluetooth skipanir. Fyrir flesta notendur eru sjálfgefin gildi fullnægjandi.
4.  Smelltu á **"Submit"** ("Senda") til að ljúka stillingunni.

## Valkostir

Eftir að þú hefur stillt MiPower rofann þinn geturðu breytt tímasetningarstillingunum hvenær sem er.

1.  Farðu í **Settings > Devices & Services** (Stillingar > Tæki og þjónustur).
2.  Finndu MiPower samþættinguna og smelltu á **"Configure"** ("Stilla").
3.  Stilltu rennibrautir fyrir *debounce*, tímamörk og tafir eftir þörfum.

## Skýring á Tímasetningarstillingum

Í stillingar- eða valmyndinni getur þú fínstillt tímasetningu Bluetooth skipana. Fyrir flesta notendur virka sjálfgefin gildi vel.

- **Turn-On Debounce (Töf við Kveikingu):** Lágmarks tími (í sekúndum) sem verður að líða áður en hægt er að framkvæma 'kveikja' skipunina aftur. Þetta kemur í veg fyrir að tækið sé ofhlaðið með vakningarmerkjum ef rofanum er snúið hratt.

- **Turn-Off Debounce (Töf við Slökkun):** Lágmarks tími (í sekúndum) sem verður að líða áður en hægt er að framkvæma 'slökkva' skipunina aftur. 

- **Delay Between Commands (Töf milli Skipana):** Mjög stutt töf (í sekúndum) milli þess að senda samfellda skipanir til `bluetoothctl` tólsins. Á sumum kerfum getur smá hlé bætt áreiðanleika.

- **Process Spawn Timeout (Tímamörk fyrir ferli ræsingu):** Hámarks tími (í sekúndum) til að bíða eftir að `bluetoothctl` ferlið byrji. Ef það mistekst að byrja innan þessa tíma mun kveikjutilraunin mistakast.

- **Pairing Timeout (Tímamörk fyrir Pörun):** Í einfaldaðri kveikjulógík er þetta tíminn sem á að bíða eftir að senda `pair` skipunina áður en gengið er út frá árangri. Það gefur tækinu tíma til að vinna úr vakningarmerkinu.

- **Bluetooth Scan Duration (Lengd Bluetooth skönnunar):** Lengdin (í sekúndum) sem samþættingin mun skanna eftir Bluetooth tækjum áður en reynt er að senda pörunarskipunina. Lengri skönnun getur hjálpað til við að finna tæki sem eru sein til að auglýsa tilvist sína.

## Lestu á þínu eigin tungumáli

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